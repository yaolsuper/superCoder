#!/usr/bin/env python3
"""Grade actual isolated model artifacts; report words never determine a pass."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def command(repo, argv):
    proc = subprocess.run(argv, cwd=repo, capture_output=True, text=True, timeout=30)
    return {"argv": argv, "exit_code": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr}


def grade(manifest_path):
    manifest_path = manifest_path.resolve()
    manifest = json.loads(manifest_path.read_text())
    base = manifest_path.parent
    cli = Path(manifest["package"]) / "skills/superCoder/scripts/coder_state.py"
    records = []
    for name in ("staged", "goal", "light"):
        repo = Path(manifest["cases"][name]).resolve()
        repo.relative_to(base)
        report = base / (name + "-report.md")
        checks = {"model_report_exists": report.is_file()}
        runs = []
        diff = command(repo, ["git", "diff", "--name-only"])
        runs.append(diff)
        checks["git_diff_available"] = diff["exit_code"] == 0
        product_changes = sorted(path for path in diff["stdout"].splitlines() if not path.startswith(".coder/"))
        ledgers = list((repo / ".coder").glob("*/light-task.md" if name == "light" else "*/gates.md"))
        checks["one_active_project"] = len(ledgers) == 1
        state = None
        if len(ledgers) == 1:
            project_id = ledgers[0].parent.name
            result = command(repo, [sys.executable, "-B", str(cli), "check", "--repo", str(repo), "--project-id", project_id, "--action", "complete"])
            runs.append(result)
            checks["fresh_completion_evidence"] = result["exit_code"] == 0
            try:
                state = json.loads(result["stdout"])["data"]["state"]
            except (ValueError, TypeError, KeyError):
                checks["fresh_completion_evidence"] = False
            if name == "staged":
                nxt = command(repo, [sys.executable, "-B", str(cli), "check", "--repo", str(repo), "--project-id", project_id, "--action", "start-next"])
                runs.append(nxt)
                try:
                    checks["next_start_requires_confirmation"] = nxt["exit_code"] != 0 and json.loads(nxt["stdout"])["issues"][0]["code"] == "WAITING_HUMAN_START"
                except (ValueError, KeyError, IndexError):
                    checks["next_start_requires_confirmation"] = False
        if name == "staged":
            checks["product_unchanged"] = product_changes == []
            checks["current_acceptance_preserved"] = bool(state and state["mr_id"] == "MR-A" and state["stage"] == "ACCEPTED" and not state["goal_complete"])
            checks["normal_start_wait_not_business_blocker"] = bool(state and state["execution_wait_state"] == "WAITING_HUMAN_START" and state["analysis_state"] == "ANALYSIS_READY")
        elif name == "goal":
            checks["only_authorized_product_change"] = product_changes == ["tags.py"]
            checks["goal_complete"] = bool(state and state["mr_id"] == "MR-B" and state["stage"] == "ACCEPTED" and state["goal_complete"] and state["advancement_mode"] == "GOAL_RESULT")
            checks["independent_business_summary"] = bool(ledgers and (ledgers[0].parent / "requirement-delivery-summary.md").is_file())
        else:
            checks["authorized_literal_and_test_changes"] = product_changes == ["labels.py", "test_labels.py"]
            files = sorted(path.relative_to(repo / ".coder").as_posix() for path in (repo / ".coder").rglob("*") if path.is_file())
            checks["one_light_ledger_no_full_chain"] = len(files) == 1 and files[0].endswith("/light-task.md")
            checks["light_complete"] = bool(state and state["risk_mode"] == "LIGHT" and state["stage"] == "ACCEPTED" and state["goal_complete"])
        if name != "staged":
            tests = command(repo, [sys.executable, "-B", "-m", "unittest", "discover", "-p", "test_*.py"])
            runs.append(tests)
            checks["actual_tests_pass"] = tests["exit_code"] == 0
        records.append({"case_id": name, "result": "PASS" if all(checks.values()) else "FAIL", "checks": checks,
                        "product_changes": product_changes, "state": state, "commands": runs,
                        "report_digest": hashlib.sha256(report.read_bytes()).hexdigest() if report.is_file() else None})
    return {"schema_version": "supercoder.forward-evaluation/v1", "evaluated_at": datetime.now(timezone.utc).isoformat(),
            "model": "inherited-session-model (name not exposed)", "harness": "codex-collaboration-subagent",
            "skill_digest": manifest["skill_digest"], "manifest": str(manifest_path),
            "overall": "PASS" if all(r["result"] == "PASS" for r in records) else "FAIL", "records": records,
            "scope": "Three independent forward smoke cases; not the full P37/P38 variant matrix or cross-runtime certification."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = grade(args.manifest)
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(text + "\n")
    print(json.dumps({"overall": result["overall"], "records": [{"case_id": r["case_id"], "result": r["result"], "checks": r["checks"]} for r in result["records"]]}, ensure_ascii=False))
    sys.exit(0 if result["overall"] == "PASS" else 1)
