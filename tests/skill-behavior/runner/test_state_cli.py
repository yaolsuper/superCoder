from __future__ import annotations

import copy
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
CLI = ROOT / "skills/superCoder/scripts/coder_state.py"
spec = importlib.util.spec_from_file_location("coder_state", CLI)
state_cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(state_cli)


def sample_state(risk="STANDARD", mode="STAGED_CHECK"):
    return {
        "schema_version": "supercoder.state/v1", "development_project_id": "demo", "mr_id": "MR-A",
        "risk_mode": risk, "stage": "RUNNING", "stage_epoch": 1,
        "advancement_mode": mode, "confirmation_unit": "mr", "execution_mode": "continuous_project",
        "execution_wait_state": "NONE", "authorization_ref": "user:implement-A-and-B",
        "goal_complete": False, "allowed_paths": ["app.py", "extra.py"], "forbidden_paths": ["secrets/**"],
        "code_paths": ["app.py"], "analysis_gate": "PASSED", "analysis_state": "ANALYSIS_READY",
        "blocking_question_count": 0, "unresolved_semantic_decision_count": 0, "unsupported_negative_constraint_count": 0,
        "source_chain": {"analysis": "analysis/a.md", "plan": "plans/a.md", "mr": "plans/a.md"},
        "artifact_strategy": "SINGLE_MR_PLAN", "plan_confirmation": "CONFIRMED",
        "checkpoints": {"CP2": "PASS", "CP3": "PASS", "CP4": "PASS", "CP5": "PASS"},
    }


class StateCliTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name) / "repo"
        self.repo.mkdir()
        (self.repo / "app.py").write_text("value = 1\n")
        self.project = self.repo / ".coder/demo"
        self.project.mkdir(parents=True)
        for name in ("analysis/a.md", "plans/a.md", "mrs/b.md", "handoff.md", "context-summary.md", "task-state.md", "reviews/a.md", "validation/a.md"):
            path = self.project / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("Fixture: real record for this isolated test.\n")

    def tearDown(self):
        self.temp.cleanup()

    def cli(self, command, *extra, root=None):
        args = [sys.executable, "-B", str(CLI), command, "--repo", str(self.repo), "--project-id", "demo", *extra]
        if root is not None:
            args += ["--artifact-root", str(root)]
        proc = subprocess.run(args, text=True, capture_output=True)
        return proc.returncode, json.loads(proc.stdout)

    def input(self, state):
        path = self.repo / "input.json"
        path.write_text(json.dumps(state))
        return str(path)

    def init(self, state):
        code, body = self.cli("init", "--input", self.input(state))
        self.assertEqual(0, code, body)

    def bind(self, state, inline=False):
        code = state_cli.code_digest(self.repo, self.project, state)
        for key, path, result in (("review", "reviews/a.md", "PASS"), ("validation", "validation/a.md", "PASSED")):
            if inline:
                path = "light-task.md"
            state[key] = {"path": path, "result": result, "code_digest": code,
                          "evidence_digest": state_cli.evidence_digest(self.project / path), "command": "python3 app.py"}
        return state

    def replace_state(self, state):
        names = ("light-task.md",) if state["risk_mode"] == "LIGHT" else state_cli.FILES
        for name in names:
            path = self.project / name
            path.write_text(state_cli.render(path.read_text(), state))

    def next_state(self, mode):
        state = sample_state(mode=mode)
        self.init(state)
        state = self.bind(state)
        state["stage"] = "ACCEPTED"
        state["next_unit"] = {"unit_id": "MR-B", "contract_revision": 2, "contract_path": "mrs/b.md", "cp4": "PASS", "dependency_evidence": []}
        self.replace_state(state)
        return state

    def test_inline_plan_edit_does_not_require_duplicate_mr(self):
        self.init(sample_state())
        self.assertEqual(0, self.cli("check", "--action", "edit", "--path", "app.py")[0])
        self.assertFalse((self.project / "mrs/a.md").exists())
        self.assertNotEqual(0, self.cli("check", "--action", "edit", "--path", "extra.py")[0])

    def test_light_completion_has_one_state_file_and_no_cp5_requirement(self):
        state = sample_state(risk="LIGHT")
        state.pop("checkpoints")
        self.init(state)
        state = self.bind(state, inline=True)
        state["stage"] = "ACCEPTED"
        state["goal_complete"] = True
        code, body = self.cli("transition", "--input", self.input({**state, "stage_epoch": 2}), "--expected-epoch", "1")
        self.assertEqual(0, code, body)
        self.assertEqual(0, self.cli("check", "--action", "complete")[0])
        self.assertFalse((self.project / "gates.md").exists())
        self.assertFalse((self.project / "requirement-delivery-summary.md").exists())

    def test_failed_or_stale_evidence_blocks_completion(self):
        state = sample_state()
        self.init(state)
        self.bind(state)
        self.replace_state(state)
        self.assertEqual(0, self.cli("check", "--action", "complete")[0])
        (self.repo / "app.py").write_text("value = 2\n")
        code, body = self.cli("check", "--action", "complete")
        self.assertNotEqual(0, code)
        self.assertEqual("VERIFICATION_STALE", body["issues"][0]["code"])

    def test_changed_evidence_record_and_missing_counter_are_not_accepted(self):
        state = sample_state()
        self.init(state)
        self.bind(state)
        self.replace_state(state)
        (self.project / "validation/a.md").write_text("changed after review\n")
        self.assertEqual("EVIDENCE_STALE", self.cli("check", "--action", "complete")[1]["issues"][0]["code"])
        state.pop("blocking_question_count")
        self.replace_state(state)
        self.assertEqual("ANALYSIS_GATE_FAILED", self.cli("check", "--action", "edit", "--path", "app.py")[1]["issues"][0]["code"])

    def test_staged_next_unit_requires_current_revision_confirmation(self):
        state = self.next_state("STAGED_CHECK")
        for approval in ({}, {"state": "CONFIRMED", "unit_id": "MR-B", "contract_revision": 1, "answer_ref": "user:yes"},
                         {"state": "CONSUMED", "unit_id": "MR-B", "contract_revision": 2, "answer_ref": "user:yes"}):
            state["next_unit_approval"] = approval
            self.replace_state(state)
            self.assertEqual("WAITING_HUMAN_START", self.cli("check", "--action", "start-next")[1]["issues"][0]["code"])
        state["next_unit_approval"] = {"state": "CONFIRMED", "unit_id": "MR-B", "contract_revision": 2, "answer_ref": "user:start-MR-B"}
        self.replace_state(state)
        candidate = {**state, "stage_epoch": 2, "stage": "RUNNING", "mr_id": "MR-B", "next_unit": None}
        code, body = self.cli("transition", "--input", self.input(candidate), "--expected-epoch", "1")
        self.assertEqual(0, code, body)
        self.assertEqual("CONSUMED", body["data"]["state"]["next_unit_approval"]["state"])

    def test_goal_mode_advances_without_human_answer_but_respects_scope_and_dependencies(self):
        state = self.next_state("GOAL_RESULT")
        self.assertEqual(0, self.cli("check", "--action", "start-next")[0])
        state["execution_mode"] = "single_mr"
        self.replace_state(state)
        self.assertEqual("NEXT_UNIT_OUT_OF_SCOPE", self.cli("check", "--action", "start-next")[1]["issues"][0]["code"])
        state["execution_mode"] = "continuous_project"
        state["next_unit"]["dependency_evidence"] = [{"path": "validation/a.md", "result": "PASS", "evidence_digest": "0" * 64}]
        self.replace_state(state)
        self.assertEqual("EVIDENCE_STALE", self.cli("check", "--action", "start-next")[1]["issues"][0]["code"])

    def test_epoch_drift_and_compare_and_swap_preserve_state(self):
        state = sample_state()
        self.init(state)
        before = {name: (self.project / name).read_bytes() for name in state_cli.FILES}
        candidate = {**state, "stage_epoch": 2, "stage": "VERIFYING"}
        self.assertEqual("STATE_WRITE_CONFLICT", self.cli("transition", "--input", self.input(candidate), "--expected-epoch", "0")[1]["issues"][0]["code"])
        self.assertEqual(before, {name: (self.project / name).read_bytes() for name in state_cli.FILES})
        path = self.project / "project-progress.md"
        path.write_text(state_cli.render(path.read_text(), {**state, "stage_epoch": 7}))
        self.assertEqual("STATUS_CONSISTENCY_FAIL", self.cli("check")[1]["issues"][0]["code"])

    def test_live_writer_lock_is_not_stolen(self):
        self.init(sample_state())
        (self.project / ".state.lock").write_text(json.dumps({"pid": os.getpid()}))
        self.assertEqual("STATE_LOCKED", self.cli("recover")[1]["issues"][0]["code"])

    def interrupt_commit(self):
        state = sample_state()
        self.init(state)
        _, old = state_cli.load(self.project)
        new = {name: state_cli.render(text, {**state, "stage_epoch": 2, "stage": "VERIFYING"}) for name, text in old.items()}
        writer = state_cli.atomic_write
        def interrupted(path, text):
            if path.name == "coder-current-task.md":
                raise KeyboardInterrupt("simulated interruption after gates write")
            writer(path, text)
        with patch.object(state_cli, "atomic_write", side_effect=interrupted):
            with self.assertRaises(KeyboardInterrupt):
                state_cli.commit(self.project, old, new)

    def test_interruption_blocks_edits_until_recovery_rolls_forward(self):
        self.interrupt_commit()
        self.assertEqual("STATE_TRANSACTION_PENDING", self.cli("check", "--action", "edit", "--path", "app.py")[1]["issues"][0]["code"])
        code, body = self.cli("recover")
        self.assertEqual(0, code, body)
        self.assertTrue(body["data"]["recovered"])
        self.assertEqual(2, self.cli("check")[1]["data"]["state"]["stage_epoch"])

    def test_recovery_does_not_overwrite_external_change(self):
        self.interrupt_commit()
        path = self.project / "project-progress.md"
        path.write_text("external change\n")
        self.assertEqual("STATE_RECOVERY_CONFLICT", self.cli("recover")[1]["issues"][0]["code"])
        self.assertEqual("external change\n", path.read_text())
        self.assertTrue((self.project / ".state-transaction.json").exists())

    def test_init_failure_rolls_back_partial_files(self):
        args = type("Args", (), {"command": "init", "repo": str(self.repo), "artifact_root": None,
                                "project_id": "demo", "input": self.input(sample_state())})()
        writer = state_cli.atomic_write
        def failed(path, text):
            if path.name == "coder-current-task.md":
                raise OSError("simulated filesystem failure")
            writer(path, text)
        with patch.object(state_cli, "atomic_write", side_effect=failed):
            with self.assertRaises(OSError):
                state_cli.execute(args)
        self.assertFalse(any((self.project / name).exists() for name in state_cli.FILES))
        self.assertFalse((self.project / ".state-transaction.json").exists())

    def test_scope_symlink_and_shared_root(self):
        state = sample_state()
        self.init(state)
        outside = self.repo.parent / "outside.py"
        outside.write_text("outside\n")
        (self.repo / "extra.py").symlink_to(outside)
        state["code_paths"].append("extra.py")
        self.replace_state(state)
        self.assertEqual("INVALID_SCOPE", self.cli("snapshot")[1]["issues"][0]["code"])
        shared = self.repo.parent / "shared"
        shared.mkdir()
        self.project.rename(shared / "demo")
        state["code_paths"] = ["app.py"]
        for name in state_cli.FILES:
            path = shared / "demo" / name
            path.write_text(state_cli.render(path.read_text(), state))
        self.assertEqual(0, self.cli("check", "--action", "edit", "--path", "app.py", root=shared)[0])

    def test_goal_summary_and_legacy_ledgers_are_not_silently_accepted(self):
        state = sample_state()
        self.init(state)
        self.bind(state)
        state["goal_complete"] = True
        self.replace_state(state)
        self.assertEqual("DELIVERY_SUMMARY_MISSING", self.cli("check", "--action", "complete")[1]["issues"][0]["code"])
        (self.project / "gates.md").write_text("legacy status: ACCEPTED\n")
        self.assertEqual("STATE_FORMAT_UNSUPPORTED", self.cli("check")[1]["issues"][0]["code"])
        self.assertEqual("STATE_ALREADY_EXISTS", self.cli("init", "--input", self.input(state))[1]["issues"][0]["code"])


if __name__ == "__main__":
    unittest.main()
