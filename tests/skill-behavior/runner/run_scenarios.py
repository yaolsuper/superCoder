#!/usr/bin/env python3
"""Run deterministic behavior scenarios without turning missing execution into PASS."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "supercoder.behavior-result/v1"
REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
VALIDATOR_PATH = REPOSITORY_ROOT / "skills/superCoder/scripts/validate_package.py"
TRACE_VALIDATOR_PATH = REPOSITORY_ROOT / "skills/superCoder/scripts/validate_trace_contract.py"
SCENARIOS_PATH = REPOSITORY_ROOT / "tests/skill-behavior/scenarios.yaml"


def load_validator():
    spec = importlib.util.spec_from_file_location("supercoder_validate_package", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load validator: {VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_trace_validator():
    spec = importlib.util.spec_from_file_location("supercoder_trace_validator", TRACE_VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load validator: {TRACE_VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_scenarios() -> list[dict[str, Any]]:
    return load_validator().parse_scenarios(SCENARIOS_PATH)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def current_commit() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "--verify", "HEAD"],
        cwd=REPOSITORY_ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=5,
    )
    return completed.stdout.strip() if completed.returncode == 0 else "UNAVAILABLE"


def score_scenario(scenario: dict[str, Any], raw_output: str | None) -> dict[str, Any]:
    expected = [str(value) for value in scenario.get("expected_verdicts", [])]
    forbidden = [str(value) for value in scenario.get("must_not", [])]
    if raw_output is None:
        return {
            "result": "NOT_RUN",
            "expected_verdicts_missing": expected,
            "forbidden_outcomes_present": [],
        }
    missing = [value for value in expected if value not in raw_output]
    present = [value for value in forbidden if value in raw_output]
    return {
        "result": "PASS" if not missing and not present else "FAIL",
        "expected_verdicts_missing": missing,
        "forbidden_outcomes_present": present,
    }


def build_result_record(
    *,
    scenario: dict[str, Any],
    raw_output: str | None,
    model: str,
    harness: str,
    commit: str,
    started_at: str,
    finished_at: str,
    adapter_version: str | None = None,
) -> dict[str, Any]:
    score = score_scenario(scenario, raw_output)
    return {
        "schema_version": SCHEMA_VERSION,
        "scenario_id": scenario["id"],
        "model": model,
        "harness": harness,
        "adapter_version": adapter_version,
        "commit": commit,
        "started_at": started_at,
        "finished_at": finished_at,
        "raw_output_digest": (
            hashlib.sha256(raw_output.encode("utf-8")).hexdigest() if raw_output is not None else None
        ),
        "result": score["result"],
        "score": {
            "expected_verdicts_missing": score["expected_verdicts_missing"],
            "forbidden_outcomes_present": score["forbidden_outcomes_present"],
        },
    }


def scenario_number(scenario_id: str) -> int | None:
    prefix = scenario_id.split("-", 1)[0]
    if prefix.startswith("p") and prefix[1:].isdigit():
        return int(prefix[1:])
    return None


def select_scenarios(scenarios: list[dict[str, Any]], selector: str) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    tokens = [token.strip().lower() for token in selector.split(",") if token.strip()]
    for token in tokens:
        if "-p" in token and token.startswith("p"):
            start_text, end_text = token.split("-p", 1)
            if start_text[1:].isdigit() and end_text.isdigit():
                start, end = int(start_text[1:]), int(end_text)
                selected.extend(
                    scenario
                    for scenario in scenarios
                    if (number := scenario_number(str(scenario["id"]))) is not None
                    and start <= number <= end
                )
                continue
        selected.extend(scenario for scenario in scenarios if str(scenario["id"]).startswith(f"{token}-"))
    unique = {str(scenario["id"]): scenario for scenario in selected}
    return sorted(unique.values(), key=lambda scenario: (scenario_number(str(scenario["id"])) or 0, scenario["id"]))


def run_p16(repository_root: Path) -> str:
    validation = load_validator().validate_repository(repository_root)
    verdicts = []
    if validation["status"] == "PASS":
        verdicts = ["CANONICAL_DISCOVERY_PASS", "REGISTRY_CONSISTENCY_PASS"]
    return json.dumps(
        {"validation": validation, "verdicts": verdicts},
        ensure_ascii=False,
        sort_keys=True,
    )


def run_trace_scenario(scenario_id: str) -> str:
    import copy
    fixture = REPOSITORY_ROOT / "tests/skill-behavior/fixtures/trace-contract/valid/manifest.json"
    data = json.loads(fixture.read_text(encoding="utf-8"))
    validator = load_trace_validator()
    verdicts: list[str] = []
    if scenario_id.startswith("p17-"):
        valid = validator.validate_manifest(data)["status"] == "PASS"
        broken = copy.deepcopy(data); broken["relations"][0]["target_ref"] += "-missing"
        codes = {item["code"] for item in validator.validate_manifest(broken)["issues"]}
        if valid and "REF_UNRESOLVED" in codes: verdicts.append("TRACE_ID_REFERENCE_INTEGRITY_PASS")
    elif scenario_id.startswith("p18-"):
        broken = copy.deepcopy(data); broken["relations"] = [r for r in broken["relations"] if r["type"] != "ARGUMENT_SUPPORTED_BY_EVIDENCE"]
        codes = {item["code"] for item in validator.validate_manifest(broken)["issues"]}
        if "CARDINALITY_VIOLATION" in codes: verdicts.append("CLAIM_ARGUMENT_EVIDENCE_PASS")
    return json.dumps({"verdicts": verdicts}, ensure_ascii=False, sort_keys=True)


def run_unit_behavior(scenario_id: str) -> str:
    suites = {
        19: ("test_knowledge_cli.py", "CARD_SECTION_CONTRACT_PASS"),
        20: ("test_knowledge_cli.py", "PRODUCT_MODULE_GOVERNANCE_PASS"),
        21: ("test_knowledge_cli.py", "CLI_PROGRESSIVE_LOADING_PASS"),
        22: ("test_knowledge_index.py", "DERIVED_INDEX_ATOMIC_REBUILD_PASS"),
        23: ("test_planning_trace.py", "ANALYSIS_CARD_PLAN_TRACE_PASS"),
        24: ("test_operation_lineage.py", "OPERATION_LINEAGE_PASS"),
        25: ("test_completion_materialization.py", "COMPLETION_GRAPH_RECONCILIATION_PASS"),
        26: ("test_completion_materialization.py", "RISK_RECOMMENDATION_CLASSIFICATION_PASS"),
    }
    number = scenario_number(scenario_id)
    filename, verdict = suites[number]
    completed = subprocess.run(
        [sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests/skill-behavior/runner", "-p", filename],
        cwd=REPOSITORY_ROOT, check=False, capture_output=True, text=True, timeout=30,
    )
    verdicts = [verdict] if completed.returncode == 0 else []
    return json.dumps({"returncode": completed.returncode, "verdicts": verdicts}, ensure_ascii=False, sort_keys=True)


def run_p27(adapter_override: str | None = None) -> tuple[str, str]:
    adapters = [adapter_override] if adapter_override else ["app-agent", "opencode"]
    adapter_script = REPOSITORY_ROOT / "tests/skill-behavior/runner/adapter_runner.py"
    fixture = REPOSITORY_ROOT / "tests/skill-behavior/fixtures/knowledge-cli/valid-repo"
    normalized: dict[str, list[dict[str, Any]]] = {}
    with tempfile.TemporaryDirectory() as directory:
        repo = Path(directory) / "repo"; shutil.copytree(fixture, repo)
        commands = [
            ["rebuild-index", "--repo", str(repo)],
            ["find", "--module", "module-1", "--limit", "5", "--repo", str(repo)],
            *[["section", "--project-id", "demo-20260715", "--section", section, "--repo", str(repo)] for section in ("changes", "risks", "relationships")],
            ["entity", "--project-id", "demo-20260715", "--entity-id", "evidence-1", "--repo", str(repo)],
        ]
        for adapter in adapters:
            normalized[adapter] = []
            for command in commands:
                proc = subprocess.run([sys.executable, "-B", str(adapter_script), "--adapter", adapter, "--", *command], cwd=REPOSITORY_ROOT, capture_output=True, text=True, timeout=30)
                try: body = json.loads(proc.stdout)
                except json.JSONDecodeError: body = {"parse_error": True}
                normalized[adapter].append({"exit_code": proc.returncode, "body": body})
    values = list(normalized.values()); equal = all(value == values[0] for value in values[1:])
    passed = equal and all(item["exit_code"] == 0 and item["body"].get("status") == "PASS" for value in values for item in value)
    verdicts = ["CROSS_HARNESS_REQUIREMENT_GRAPH_E2E_PASS"] if passed else []
    raw = json.dumps({"adapters": adapters, "semantic_equal": equal, "normalized": normalized, "verdicts": verdicts}, ensure_ascii=False, sort_keys=True)
    return raw, adapters[0] if len(adapters) == 1 else "app-agent+opencode"


def execute_scenario(scenario: dict[str, Any], repository_root: Path, harness_override: str | None = None) -> tuple[str | None, str, str]:
    if str(scenario["id"]).startswith("p16-"):
        return run_p16(repository_root), "deterministic-validator", "stdlib-package-validator"
    if str(scenario["id"]).startswith(("p17-", "p18-")):
        return run_trace_scenario(str(scenario["id"])), "deterministic-validator", "stdlib-trace-validator"
    number = scenario_number(str(scenario["id"]))
    if number is not None and 19 <= number <= 26:
        return run_unit_behavior(str(scenario["id"])), "deterministic-unittest", "stdlib-knowledge-suite"
    if number == 27:
        raw, harness = run_p27(harness_override)
        return raw, "adapter-contract-runner", harness
    return None, "not-executed", "none"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", required=True, help="P16, P1-P16, or comma-separated selectors")
    parser.add_argument("--format", choices=("json", "text"), default="text")
    parser.add_argument("--repo", default=str(REPOSITORY_ROOT), help="repository root for deterministic scenarios")
    parser.add_argument("--harness", choices=("app-agent", "opencode"), help="execute P27 through one adapter")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    scenarios = select_scenarios(load_scenarios(), args.scenario)
    if not scenarios:
        print(f"no scenarios matched: {args.scenario}", file=sys.stderr)
        return 2

    records: list[dict[str, Any]] = []
    for scenario in scenarios:
        started_at = utc_now()
        raw_output, model, harness = execute_scenario(scenario, Path(args.repo).resolve(), args.harness)
        records.append(
            build_result_record(
                scenario=scenario,
                raw_output=raw_output,
                model=model,
                harness=harness,
                commit=current_commit(),
                started_at=started_at,
                finished_at=utc_now(),
                adapter_version="1" if str(scenario["id"]).startswith("p27-") else None,
            )
        )

    results = [record["result"] for record in records]
    overall = "FAIL" if "FAIL" in results else "PASS" if set(results) == {"PASS"} else "PARTIAL"
    envelope = {"schema_version": SCHEMA_VERSION, "overall": overall, "records": records}
    if args.format == "json":
        print(json.dumps(envelope, ensure_ascii=False, sort_keys=True, indent=2))
    else:
        print(f"behavior scenarios: {overall}")
        for record in records:
            print(f"{record['scenario_id']}: {record['result']} ({record['harness']})")
    return 1 if overall == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
