#!/usr/bin/env python3
"""Check Markdown ledger state and perform recoverable, serialized transitions."""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import re
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path

SCHEMA = "supercoder.state/v1"
MARKER = re.compile(r"<!-- sc:state -->\s*```json\s*(.*?)\s*```\s*<!-- /sc:state -->", re.S)
FILES = ("gates.md", "coder-current-task.md", "project-progress.md")
STAGES = {"ANALYZING", "ANALYSIS_READY", "PLANNING", "MR_SPLIT", "READY", "RUNNING", "VERIFYING", "ACCEPTED", "BLOCKED", "BLOCKED_HUMAN_CONFIRMATION", "HUMAN_INPUT_RECEIVED"}


class StateError(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


def digest(value):
    return hashlib.sha256(value).hexdigest()


def scoped(root, relative):
    path = (root / relative).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError:
        raise StateError("INVALID_SCOPE", f"path escapes selected root: {relative}")
    return path


def project_path(repo, artifact_root, project_id):
    if not project_id or project_id in (".", "..") or "/" in project_id or "\\" in project_id:
        raise StateError("INVALID_SCOPE", "project ID must be a single directory name")
    root = Path(artifact_root) if artifact_root is not None else Path(".coder")
    if artifact_root is not None and not str(artifact_root).strip():
        raise StateError("INVALID_SCOPE", "artifact root must not be empty")
    root = (root if root.is_absolute() else repo / root).resolve()
    return scoped(root, project_id)


def validate_shape(state):
    if not isinstance(state, dict) or state.get("schema_version") != SCHEMA:
        raise StateError("STATE_FORMAT_UNSUPPORTED", "explicit supercoder.state/v1 block required; legacy ledgers are not silently migrated")
    for key in ("development_project_id", "mr_id", "authorization_ref"):
        if not isinstance(state.get(key), str) or not state[key].strip():
            raise StateError("STATE_FIELD_MISSING", key)
    if type(state.get("stage_epoch")) is not int or state["stage_epoch"] < 0:
        raise StateError("STATE_FIELD_INVALID", "stage_epoch")
    if state.get("stage") not in STAGES or state.get("risk_mode") not in ("LIGHT", "STANDARD", "CONTROLLED"):
        raise StateError("STATE_FIELD_INVALID", "stage or risk_mode")
    if state.get("advancement_mode") not in ("STAGED_CHECK", "GOAL_RESULT") or state.get("confirmation_unit") not in ("mr", "task"):
        raise StateError("ADVANCEMENT_MODE_CONFLICT", "mode or confirmation boundary is invalid")
    if state.get("execution_mode") not in ("single_mr", "continuous_project"):
        raise StateError("STATE_FIELD_INVALID", "execution_mode")
    if type(state.get("goal_complete")) is not bool:
        raise StateError("STATE_FIELD_INVALID", "goal_complete")
    if state.get("execution_wait_state") not in ("NONE", "WAITING_HUMAN_START"):
        raise StateError("STATE_FIELD_INVALID", "execution_wait_state")
    for key in ("allowed_paths", "forbidden_paths", "code_paths"):
        if not isinstance(state.get(key), list) or not all(isinstance(x, str) and x for x in state[key]):
            raise StateError("STATE_FIELD_INVALID", key)
    if not state["allowed_paths"] or not state["code_paths"]:
        raise StateError("STATE_FIELD_MISSING", "allowed_paths and code_paths must not be empty")
    if state["risk_mode"] == "LIGHT" and state.get("task_kind") in ("BUG", "HOTFIX", "INCIDENT", "MIGRATION"):
        raise StateError("MODE_UPGRADE_REQUIRED", "task kind cannot use LIGHT")


def parse(text):
    if text.count("<!-- sc:state -->") != 1 or text.count("<!-- /sc:state -->") != 1:
        raise StateError("STATE_FORMAT_UNSUPPORTED", "one balanced machine state block is required")
    match = MARKER.search(text)
    if not match:
        raise StateError("STATE_FORMAT_UNSUPPORTED", "invalid state block")
    state = json.loads(match.group(1))
    validate_shape(state)
    return state


def render(text, state):
    block = "<!-- sc:state -->\n```json\n" + json.dumps(state, ensure_ascii=False, sort_keys=True, indent=2) + "\n```\n<!-- /sc:state -->"
    return MARKER.sub(lambda _: block, text) if MARKER.search(text) else text.rstrip() + "\n\n" + block + "\n"


def load(project):
    if scoped(project, ".state-transaction.json").exists():
        raise StateError("STATE_TRANSACTION_PENDING", "run recover before editing code or advancing")
    light = scoped(project, "light-task.md")
    if light.exists():
        if any(scoped(project, name).exists() for name in FILES):
            raise StateError("STATE_FORMAT_UNSUPPORTED", "archive the LIGHT state block explicitly before upgrading")
        state = parse(light.read_text())
        if state["risk_mode"] != "LIGHT":
            raise StateError("STATUS_CONSISTENCY_FAIL", "light-task has non-LIGHT mode")
        return state, {"light-task.md": light.read_text()}
    texts = {}
    for name in FILES:
        path = scoped(project, name)
        if not path.is_file():
            raise StateError("LEDGER_INCOMPLETE", name)
        texts[name] = path.read_text()
    states = [parse(texts[name]) for name in FILES]
    if any(state != states[0] for state in states[1:]):
        raise StateError("STATUS_CONSISTENCY_FAIL", "machine state projections differ")
    if states[0]["risk_mode"] == "LIGHT":
        raise StateError("STATUS_CONSISTENCY_FAIL", "LIGHT must use light-task.md")
    return states[0], texts


def product_path(repo, project, relative, state):
    repo, project = repo.resolve(), project.resolve()
    if Path(relative).is_absolute() or ".." in Path(relative).parts:
        raise StateError("PATH_GUARD_FAIL", relative)
    path = scoped(repo, relative)
    rel = path.relative_to(repo).as_posix()
    if ".git" in path.relative_to(repo).parts or path == project or project in path.parents:
        raise StateError("PATH_GUARD_FAIL", "product scope must exclude Git and ledger files")
    if not any(fnmatch.fnmatchcase(rel, pat) for pat in state["allowed_paths"]) or any(fnmatch.fnmatchcase(rel, pat) for pat in state["forbidden_paths"]):
        raise StateError("PATH_GUARD_FAIL", relative)
    return path


def code_digest(repo, project, state):
    items = []
    for relative in sorted(set(state["code_paths"])):
        path = product_path(repo, project, relative, state)
        if path.exists() and not path.is_file():
            raise StateError("PATH_GUARD_FAIL", "code_paths must name files, not directories")
        items.append([relative, digest(path.read_bytes()) if path.exists() else None])
    return digest(json.dumps(items, ensure_ascii=False, separators=(",", ":")).encode())


def evidence_digest(path):
    # LIGHT review/validation lives outside its machine block, avoiding a self-hash.
    return digest(MARKER.sub("", path.read_text()).encode())


def evidence(project, record, expected, current_code=None):
    if not isinstance(record, dict) or record.get("result") != expected or not record.get("path"):
        raise StateError("COMPLETION_EVIDENCE_FAIL", "missing or unsuccessful evidence record")
    path = scoped(project, record["path"])
    if not path.is_file() or evidence_digest(path) != record.get("evidence_digest"):
        raise StateError("EVIDENCE_STALE", str(record["path"]))
    if current_code is not None and record.get("code_digest") != current_code:
        raise StateError("VERIFICATION_STALE", "evidence belongs to a different code snapshot")


def guard(repo, project, state, action, paths=()):
    validate_shape(state)
    if state["development_project_id"] != project.name:
        raise StateError("STATUS_CONSISTENCY_FAIL", "project ID does not match selected directory")
    if action == "read":
        return ["READ_CONTEXT"]
    if (state.get("analysis_gate") != "PASSED" or state.get("analysis_state") in ("BLOCKED_HUMAN_CONFIRMATION", "HUMAN_INPUT_RECEIVED")
        or any(type(state.get(k)) is not int or state[k] != 0 for k in ("blocking_question_count", "unresolved_semantic_decision_count", "unsupported_negative_constraint_count"))):
        raise StateError("ANALYSIS_GATE_FAILED", "analysis gate or required counters are unresolved")
    if state["risk_mode"] != "LIGHT":
        for name in ("handoff.md", "context-summary.md", "task-state.md"):
            if not scoped(project, name).is_file():
                raise StateError("LEDGER_INCOMPLETE", name)
        chain = state.get("source_chain", {})
        for role in ("analysis", "plan", "mr"):
            if not chain.get(role) or not scoped(project, chain[role]).is_file():
                raise StateError("SOURCE_CHAIN_FAIL", role)
        if state.get("artifact_strategy") == "SINGLE_MR_PLAN" and chain["mr"] != chain["plan"]:
            raise StateError("INLINE_MR_CONTRACT_INVALID", "inline contract must resolve to the Plan")
        if state.get("plan_confirmation") not in ("CONFIRMED", "AUTO_CHECKED"):
            raise StateError("PLAN_CONFIRMATION_REQUIRED", "plan is not confirmed")
        if state.get("plan_confirmation") == "AUTO_CHECKED" and state["advancement_mode"] != "GOAL_RESULT":
            raise StateError("ADVANCEMENT_MODE_CONFLICT", "automatic plan confirmation requires GOAL_RESULT")
        for cp in ("CP2", "CP3", "CP4"):
            if state.get("checkpoints", {}).get(cp) != "PASS":
                raise StateError("CHECKPOINT_FAIL", cp)
    if action == "edit":
        if state["stage"] != "RUNNING" or state["execution_wait_state"] != "NONE":
            raise StateError("EXECUTION_NOT_RUNNING", "current unit is not allowed to edit")
        if not paths:
            raise StateError("EDIT_PATH_REQUIRED", "check every intended product path")
        for relative in paths:
            product_path(repo, project, relative, state)
            if relative not in state["code_paths"]:
                raise StateError("PATH_GUARD_FAIL", "edited path must also be declared in code_paths")
        return ["MODIFY_PRODUCT_CODE"]
    current = code_digest(repo, project, state)
    evidence(project, state.get("review"), "PASS", current)
    evidence(project, state.get("validation"), "PASSED", current)
    if not state["validation"].get("command"):
        raise StateError("COMPLETION_EVIDENCE_FAIL", "real validation command is required")
    if state["risk_mode"] != "LIGHT" and state.get("checkpoints", {}).get("CP5") != "PASS":
        raise StateError("CHECKPOINT_FAIL", "CP5")
    if action == "complete":
        if state["goal_complete"] and state.get("next_unit"):
            raise StateError("COMPLETION_EVIDENCE_FAIL", "remaining unit contradicts goal completion")
        if state["goal_complete"] and state["risk_mode"] != "LIGHT" and not scoped(project, "requirement-delivery-summary.md").is_file():
            raise StateError("DELIVERY_SUMMARY_MISSING", "final business summary required")
        return ["ACCEPT_CURRENT_UNIT"]
    if action != "start-next" or state["stage"] != "ACCEPTED":
        raise StateError("STATE_TRANSITION_INVALID", "next unit requires current acceptance")
    if state["execution_mode"] != "continuous_project":
        raise StateError("NEXT_UNIT_OUT_OF_SCOPE", "single_mr scope does not authorize another unit")
    nxt = state.get("next_unit")
    if not isinstance(nxt, dict) or not nxt.get("unit_id") or type(nxt.get("contract_revision")) is not int or nxt.get("cp4") != "PASS":
        raise StateError("NEXT_UNIT_NOT_READY", "next contract identity, revision and CP4 are required")
    if not nxt.get("contract_path") or not scoped(project, nxt["contract_path"]).is_file():
        raise StateError("NEXT_UNIT_NOT_READY", "next contract is missing")
    if not isinstance(nxt.get("dependency_evidence"), list):
        raise StateError("NEXT_UNIT_NOT_READY", "explicit dependency evidence list required")
    for dep in nxt["dependency_evidence"]:
        evidence(project, dep, "PASS")
    if state["advancement_mode"] == "STAGED_CHECK":
        approval = state.get("next_unit_approval", {})
        if (approval.get("state") != "CONFIRMED" or approval.get("unit_id") != nxt["unit_id"]
            or approval.get("contract_revision") != nxt["contract_revision"] or not approval.get("answer_ref")):
            raise StateError("WAITING_HUMAN_START", "explicit approval for this unit/revision is required")
    elif state["execution_wait_state"] != "NONE":
        raise StateError("ADVANCEMENT_MODE_CONFLICT", "GOAL_RESULT cannot automatically bypass a recorded human wait")
    return ["START_NEXT_UNIT"]


def atomic_write(path, text):
    fd, name = tempfile.mkstemp(prefix=".state-write-", dir=path.parent)
    temp = Path(name)
    try:
        with os.fdopen(fd, "w") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, path)
    finally:
        temp.unlink(missing_ok=True)


@contextmanager
def lock(project, recover=False):
    path = scoped(project, ".state.lock")
    if recover and path.exists():
        pid = json.loads(path.read_text()).get("pid")
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            path.unlink()
        else:
            raise StateError("STATE_LOCKED", "writer is still alive; do not steal its lock")
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise StateError("STATE_LOCKED", "another writer or interrupted writer holds this project")
    with os.fdopen(fd, "w") as stream:
        json.dump({"pid": os.getpid()}, stream)
    try:
        yield
    finally:
        path.unlink(missing_ok=True)


def commit(project, old, new):
    journal = scoped(project, ".state-transaction.json")
    transaction = {"schema_version": "supercoder.state-transaction/v1", "old": old, "new": new}
    atomic_write(journal, json.dumps(transaction, ensure_ascii=False))
    try:
        for name, text in new.items():
            path = scoped(project, name)
            current = path.read_text() if path.exists() else None
            if current != old[name]:
                raise StateError("STATE_WRITE_CONFLICT", name)
            atomic_write(path, text)
    except Exception:
        # Roll back only our own writes; preserve unexpected external changes.
        for name, text in old.items():
            path = scoped(project, name)
            current = path.read_text() if path.exists() else None
            if current == new[name]:
                if text is None:
                    path.unlink()
                else:
                    atomic_write(path, text)
            elif current != text:
                raise StateError("STATE_RECOVERY_CONFLICT", "external change detected; journal retained")
        journal.unlink()
        raise
    journal.unlink()


def recover(project):
    journal = scoped(project, ".state-transaction.json")
    with lock(project, recover=True):
        if not journal.is_file():
            return {"recovered": False}
        data = json.loads(journal.read_text())
        names = set(data.get("new", {}))
        if data.get("schema_version") != "supercoder.state-transaction/v1" or names not in (set(FILES), {"light-task.md"}) or set(data.get("old", {})) != names:
            raise StateError("STATE_RECOVERY_CONFLICT", "invalid journal file set")
        states = [parse(text) for text in data["new"].values()]
        if any(s != states[0] for s in states[1:]):
            raise StateError("STATE_RECOVERY_CONFLICT", "journal projections differ")
        for name in names:
            path = scoped(project, name)
            current = path.read_text() if path.exists() else None
            if current not in (data["old"][name], data["new"][name]):
                raise StateError("STATE_RECOVERY_CONFLICT", name)
        for name, text in data["new"].items():
            atomic_write(scoped(project, name), text)
        journal.unlink()
        return {"recovered": True, "state": states[0]}


def execute(args):
    repo = Path(args.repo).resolve()
    project = project_path(repo, args.artifact_root, args.project_id)
    if args.command == "init":
        state = json.loads(Path(args.input).read_text())
        validate_shape(state)
        if state["development_project_id"] != args.project_id:
            raise StateError("STATUS_CONSISTENCY_FAIL", "project ID mismatch")
        project.mkdir(parents=True, exist_ok=True)
        with lock(project):
            if scoped(project, ".state-transaction.json").exists() or any(scoped(project, name).exists() for name in (*FILES, "light-task.md")):
                raise StateError("STATE_ALREADY_EXISTS", "init never replaces existing ledgers")
            names = ("light-task.md",) if state["risk_mode"] == "LIGHT" else FILES
            commit(project, {name: None for name in names}, {name: render(f"# {name}\n", state) for name in names})
        return {"state": state}
    if args.command == "recover":
        return recover(project)
    state, texts = load(project)
    if args.command == "snapshot":
        return {"code_digest": code_digest(repo, project, state), "evidence_digests": {name: evidence_digest(scoped(project, name)) for name in args.evidence}}
    if args.command == "check":
        return {"state": state, "allowed_actions": guard(repo, project, state, args.action, args.path)}
    candidate = json.loads(Path(args.input).read_text())
    validate_shape(candidate)
    with lock(project):
        state, texts = load(project)
        if state["stage_epoch"] != args.expected_epoch or candidate["stage_epoch"] != args.expected_epoch + 1:
            raise StateError("STATE_WRITE_CONFLICT", "epoch changed or candidate is not the next epoch")
        if candidate["risk_mode"] != state["risk_mode"]:
            raise StateError("MODE_UPGRADE_REQUIRED", "explicit artifact migration is required")
        if candidate["mr_id"] != state["mr_id"]:
            guard(repo, project, state, "start-next")
            if candidate["mr_id"] != state["next_unit"]["unit_id"]:
                raise StateError("STATE_TRANSITION_INVALID", "candidate is not the approved next unit")
            if state["advancement_mode"] == "STAGED_CHECK":
                candidate["next_unit_approval"] = {**state["next_unit_approval"], "state": "CONSUMED"}
        if candidate["stage"] == "RUNNING":
            guard(repo, project, candidate, "edit", candidate["code_paths"])
        elif candidate["stage"] == "ACCEPTED":
            guard(repo, project, candidate, "complete")
        history = "\n\n## State transition\n" + json.dumps({"from_epoch": state["stage_epoch"], "to_epoch": candidate["stage_epoch"], "unit_id": candidate["mr_id"]}, ensure_ascii=False) + "\n"
        new = {name: render(text, candidate) + (history if name == "gates.md" else "") for name, text in texts.items()}
        commit(project, texts, new)
        return {"state": candidate}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("init", "check", "snapshot", "transition", "recover"):
        sub = commands.add_parser(name)
        sub.add_argument("--repo", required=True)
        sub.add_argument("--artifact-root")
        sub.add_argument("--project-id", required=True)
        if name in ("init", "transition"):
            sub.add_argument("--input", required=True)
        if name == "transition":
            sub.add_argument("--expected-epoch", type=int, required=True)
        if name == "check":
            sub.add_argument("--action", choices=("read", "edit", "complete", "start-next"), default="read")
            sub.add_argument("--path", action="append", default=[])
        if name == "snapshot":
            sub.add_argument("--evidence", action="append", default=[])
    args = parser.parse_args(argv)
    try:
        body = {"status": "PASS", "data": execute(args), "issues": []}
        code = 0
    except (StateError, OSError, ValueError, TypeError, KeyError) as error:
        body = {"status": "FAIL", "data": None, "issues": [{"code": getattr(error, "code", "STATE_INPUT_INVALID"), "message": str(error)}]}
        code = 1
    print(json.dumps({"schema_version": "supercoder.state-cli/v1", "command": args.command, **body}, ensure_ascii=False))
    return code


if __name__ == "__main__":
    sys.exit(main())
