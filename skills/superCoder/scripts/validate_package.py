#!/usr/bin/env python3
"""Validate the distributable superCoder package with Python's stdlib only."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


SCHEMA_VERSION = "supercoder.package-validation/v1"
CANONICAL_ENTRY = "skills/superCoder/SKILL.md"
MODULE_MAP = "skills/superCoder/config/module-map.yaml"
SCENARIO_REGISTRY = "tests/skill-behavior/scenarios.yaml"
HUMAN_CONFIRMATION_SCENARIO = "p28-evidence-first-human-confirmation-gate"
HUMAN_CONFIRMATION_CONTRACT: dict[str, tuple[str, ...]] = {
    "skills/superCoder/config/human-confirmation-gate.yaml": (
        'schema_version: "supercoder.human-confirmation-gate/v1"',
        "BLOCKED_HUMAN_CONFIRMATION",
        "HUMAN_INPUT_RECEIVED",
        "ANALYSIS_READY",
        "blocking_question_without_source_point_or_evidence_gap",
        "unresolved_semantic_decision_count_is_zero",
        "unsupported_negative_constraint_count_is_zero",
        "semantic_gate_counter_missing",
        "infer_from_silence: false",
        "direct_transition_to_planning: false",
    ),
    "skills/superCoder/references/shared/human-confirmation-gate.md": (
        "证据优先扫描",
        "Source Point",
        "Evidence Gap",
        "BLOCKED_HUMAN_CONFIRMATION",
        "HUMAN_INPUT_RECEIVED",
        "ANALYZING",
        "Analysis Gate",
        "analysis_state",
        "语义维度审计",
        "负向约束来源审计",
    ),
    "skills/superCoder/assets/templates/human-confirmation.md": (
        "Scan Activity",
        "Source Point",
        "Evidence Gap",
        "Blocking Question",
        "Human Answer",
        "Decision",
        "analysis_state: BLOCKED_HUMAN_CONFIRMATION",
        "Semantic Decision Matrix",
        "Negative Constraint Inventory",
    ),
    "skills/superCoder-planning/references/planning.md": (
        "evidence_scan_status",
        "analysis_state",
        "blocking_question_count",
        "BLOCKED_HUMAN_CONFIRMATION",
        "semantic_decision_matrix",
        "negative_constraint_inventory",
    ),
    "skills/superCoder-execution/references/execution.md": (
        "analysis_gate: PASSED",
        "analysis_state",
        "blocking_question_count: 0",
        "HUMAN_INPUT_RECEIVED",
        "unresolved_semantic_decision_count: 0",
        "unsupported_negative_constraint_count: 0",
        "字段缺失不得按零处理",
    ),
    "skills/superCoder-checkpoint/references/checkpoint.md": (
        "Source Point/Evidence Gap",
        "HUMAN_INPUT_RECEIVED",
        "NEGATIVE_CONSTRAINT_SOURCE_MISSING",
    ),
    "skills/superCoder-checkpoint/references/document-review-checklist.md": (
        "语义维度完整",
        "负向约束有来源",
        "不新增无来源约束",
    ),
}


def issue(code: str, path: str, message: str) -> dict[str, str]:
    return {"code": code, "path": path, "message": message}


def normalized_relative_path(value: str) -> str | None:
    candidate = PurePosixPath(value)
    if candidate.is_absolute() or ".." in candidate.parts:
        return None
    return candidate.as_posix()


def exact_path_status(root: Path, relative_path: str) -> str:
    normalized = normalized_relative_path(relative_path)
    if normalized is None:
        return "invalid"

    current = root
    for part in PurePosixPath(normalized).parts:
        if not current.is_dir():
            return "missing"
        names = [entry.name for entry in current.iterdir()]
        if part in names:
            current = current / part
            continue
        if any(name.casefold() == part.casefold() for name in names):
            return "case_mismatch"
        return "missing"
    return "exact"


def validate_exact_path(root: Path, relative_path: str) -> list[dict[str, str]]:
    status = exact_path_status(root, relative_path)
    if status == "exact":
        return []
    if status == "case_mismatch":
        return [
            issue(
                "PATH_CASE_MISMATCH",
                relative_path,
                "path exists only with different character case",
            )
        ]
    if status == "invalid":
        return [issue("REFERENCE_INVALID", relative_path, "path must stay within repository root")]
    return [issue("REFERENCE_MISSING", relative_path, "referenced path does not exist")]


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str | None]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as error:
        return {}, f"cannot read UTF-8 frontmatter: {error}"
    if not lines or lines[0] != "---":
        return {}, "frontmatter must start on the first line"
    try:
        closing = lines.index("---", 1)
    except ValueError:
        return {}, "frontmatter closing delimiter is missing"

    fields: dict[str, str] = {}
    for line in lines[1:closing]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.fullmatch(r"([A-Za-z0-9_-]+):\s*(.*?)\s*", line)
        if not match:
            return {}, f"unsupported frontmatter line: {line}"
        key, raw_value = match.groups()
        value = raw_value.strip().strip('"\'')
        if key in fields:
            return {}, f"duplicate frontmatter field: {key}"
        fields[key] = value
    return fields, None


def validate_skill_frontmatter(root: Path) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    skill_files = sorted((root / "skills").glob("*/SKILL.md")) if (root / "skills").is_dir() else []
    if not skill_files:
        return [issue("REFERENCE_MISSING", "skills/*/SKILL.md", "no skill entry files found")]
    for path in skill_files:
        relative = path.relative_to(root).as_posix()
        fields, error = parse_frontmatter(path)
        if error:
            issues.append(issue("FRONTMATTER_INVALID", relative, error))
            continue
        missing = [key for key in ("name", "description") if not fields.get(key)]
        unexpected = sorted(set(fields) - {"name", "description"})
        if missing:
            issues.append(
                issue("FRONTMATTER_INVALID", relative, f"missing required fields: {', '.join(missing)}")
            )
        if unexpected:
            issues.append(
                issue("FRONTMATTER_INVALID", relative, f"unexpected fields: {', '.join(unexpected)}")
            )
    return issues


def parse_module_map(path: Path) -> tuple[list[str], list[str]]:
    module_ids: list[str] = []
    file_paths: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        module_match = re.fullmatch(r"\s*-\s+id:\s*([A-Za-z0-9_.-]+)\s*", line)
        if module_match:
            module_ids.append(module_match.group(1))
            continue
        path_match = re.fullmatch(r"\s*-\s+[\"']([^\"']+)[\"']\s*", line)
        if path_match:
            file_paths.append(path_match.group(1))
    return module_ids, file_paths


def duplicate_values(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return sorted(duplicates)


def parse_scenarios(path: Path) -> list[dict[str, Any]]:
    scenarios: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    current_list: str | None = None
    list_fields = {"required_routes", "expected_verdicts", "must_not"}

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        id_match = re.fullmatch(r"\s{2}-\s+id:\s*(\S+)\s*", raw_line)
        if id_match:
            current = {
                "id": id_match.group(1),
                "required_routes": [],
                "expected_verdicts": [],
                "must_not": [],
            }
            scenarios.append(current)
            current_list = None
            continue
        if current is None:
            continue
        scalar_match = re.fullmatch(r"\s{4}([A-Za-z0-9_]+):\s*(.*?)\s*", raw_line)
        if scalar_match:
            key, value = scalar_match.groups()
            if key in list_fields:
                current_list = key
            else:
                current[key] = value.strip('"\'')
                current_list = None
            continue
        item_match = re.fullmatch(r"\s{6}-\s*(.*?)\s*", raw_line)
        if item_match and current_list:
            current[current_list].append(item_match.group(1).strip('"\''))
    return scenarios


def validate_module_map(root: Path) -> tuple[list[dict[str, str]], set[str]]:
    issues: list[dict[str, str]] = []
    path = root / MODULE_MAP
    if exact_path_status(root, MODULE_MAP) != "exact":
        return validate_exact_path(root, MODULE_MAP), set()
    try:
        module_ids, paths = parse_module_map(path)
    except (OSError, UnicodeError) as error:
        return [issue("REGISTRY_DRIFT", MODULE_MAP, f"cannot parse module map: {error}")], set()
    for duplicate in duplicate_values(module_ids):
        issues.append(issue("REGISTRY_DRIFT", MODULE_MAP, f"duplicate module id: {duplicate}"))
    for relative_path in sorted(set(paths)):
        issues.extend(validate_exact_path(root, relative_path))
    return issues, set(paths)


def validate_scenario_registry(root: Path, module_paths: set[str]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    if exact_path_status(root, SCENARIO_REGISTRY) != "exact":
        return validate_exact_path(root, SCENARIO_REGISTRY)
    try:
        scenarios = parse_scenarios(root / SCENARIO_REGISTRY)
    except (OSError, UnicodeError) as error:
        return [issue("REGISTRY_DRIFT", SCENARIO_REGISTRY, f"cannot parse scenario registry: {error}")]
    ids = [str(scenario.get("id", "")) for scenario in scenarios]
    for duplicate in duplicate_values(ids):
        issues.append(issue("REGISTRY_DRIFT", SCENARIO_REGISTRY, f"duplicate scenario id: {duplicate}"))
    if not scenarios:
        issues.append(issue("REGISTRY_DRIFT", SCENARIO_REGISTRY, "no scenarios registered"))
    for scenario in scenarios:
        scenario_id = str(scenario.get("id", ""))
        markdown = str(scenario.get("markdown", ""))
        if not re.fullmatch(r"p\d+-[a-z0-9-]+", scenario_id):
            issues.append(issue("REGISTRY_DRIFT", SCENARIO_REGISTRY, f"invalid scenario id: {scenario_id}"))
        if not markdown:
            issues.append(issue("REGISTRY_DRIFT", SCENARIO_REGISTRY, f"{scenario_id} has no markdown"))
        else:
            spec_path = f"tests/skill-behavior/{markdown}"
            issues.extend(validate_exact_path(root, spec_path))
            if module_paths and spec_path not in module_paths:
                issues.append(
                    issue("REGISTRY_DRIFT", spec_path, "scenario spec is not registered in module-map.yaml")
                )
        for route in scenario.get("required_routes", []):
            issues.extend(validate_exact_path(root, str(route)))
        if not scenario.get("expected_verdicts"):
            issues.append(
                issue("REGISTRY_DRIFT", SCENARIO_REGISTRY, f"{scenario_id} has no expected verdicts")
            )
        if not scenario.get("must_not"):
            issues.append(issue("REGISTRY_DRIFT", SCENARIO_REGISTRY, f"{scenario_id} has no must_not rules"))
        if scenario_id == "p16-canonical-discovery-and-registry-consistency" and module_paths:
            required_distribution_paths = {
                "skills/superCoder/agents/openai.yaml",
                "skills/superCoder/scripts/validate_package.py",
                "tests/skill-behavior/p16-canonical-discovery-and-registry-consistency.md",
                "tests/skill-behavior/runner/run_scenarios.py",
                "tests/skill-behavior/runner/test_runner_contract.py",
                "tests/skill-behavior/runner/test_validate_package.py",
            }
            for required_path in sorted(required_distribution_paths - module_paths):
                issues.append(
                    issue("REGISTRY_DRIFT", required_path, "P16 distribution file is not in module-map.yaml")
                )
    return issues


def validate_readme_links(root: Path) -> list[dict[str, str]]:
    readme = root / "README.md"
    if not readme.is_file():
        return [issue("REFERENCE_MISSING", "README.md", "repository README is missing")]
    content = readme.read_text(encoding="utf-8")
    links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", content)
    issues: list[dict[str, str]] = []
    for target in sorted(set(links)):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        clean_target = target.split("#", 1)[0]
        issues.extend(validate_exact_path(root, clean_target))
    return issues


def validate_harness_entries(root: Path) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    for mapping in sorted((root / "harness").glob("*/tool-mapping.md")):
        content = mapping.read_text(encoding="utf-8")
        relative = mapping.relative_to(root).as_posix()
        if "skills/supercoder" in content or "`supercoder`" in content:
            issues.append(issue("PATH_CASE_MISMATCH", relative, "harness uses non-canonical supercoder entry"))
    plugin_js = root / "harness/opencode/plugin.js"
    if plugin_js.is_file() and re.search(r'entrySkill:\s*"supercoder"', plugin_js.read_text(encoding="utf-8")):
        issues.append(
            issue("PATH_CASE_MISMATCH", "harness/opencode/plugin.js", "entrySkill must be superCoder")
        )
    plugin_json = root / "harness/app-agent/plugin.json"
    if plugin_json.is_file():
        try:
            entry_skill = json.loads(plugin_json.read_text(encoding="utf-8")).get("entrySkill")
        except (json.JSONDecodeError, OSError, UnicodeError) as error:
            issues.append(issue("REGISTRY_DRIFT", "harness/app-agent/plugin.json", str(error)))
        else:
            if entry_skill != "superCoder":
                issues.append(
                    issue("PATH_CASE_MISMATCH", "harness/app-agent/plugin.json", "entrySkill must be superCoder")
                )
    return issues


def validate_openai_metadata(root: Path) -> list[dict[str, str]]:
    relative = "skills/superCoder/agents/openai.yaml"
    problems = validate_exact_path(root, relative)
    if problems:
        return problems
    content = (root / relative).read_text(encoding="utf-8")
    required_patterns = {
        "display_name": r'^\s{2}display_name:\s*"superCoder"\s*$',
        "short_description": r'^\s{2}short_description:\s*".+"\s*$',
        "default_prompt": r'^\s{2}default_prompt:\s*".*\$superCoder.*"\s*$',
    }
    issues: list[dict[str, str]] = []
    for field, pattern in required_patterns.items():
        if not re.search(pattern, content, re.MULTILINE):
            issues.append(issue("REGISTRY_DRIFT", relative, f"missing or invalid interface.{field}"))
    return issues


def validate_human_confirmation_contract(root: Path) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    for relative, required_tokens in HUMAN_CONFIRMATION_CONTRACT.items():
        path_issues = validate_exact_path(root, relative)
        issues.extend(path_issues)
        if path_issues:
            continue
        try:
            content = (root / relative).read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            issues.append(
                issue("HUMAN_CONFIRMATION_CONTRACT_INVALID", relative, f"cannot read contract: {error}")
            )
            continue
        for token in required_tokens:
            if token not in content:
                issues.append(
                    issue(
                        "HUMAN_CONFIRMATION_CONTRACT_INVALID",
                        relative,
                        f"required gate token is missing: {token}",
                    )
                )
    return issues


def validate_repository(root: Path | str) -> dict[str, Any]:
    repository_root = Path(root).resolve()
    issues: list[dict[str, str]] = []
    issues.extend(validate_exact_path(repository_root, CANONICAL_ENTRY))
    issues.extend(validate_skill_frontmatter(repository_root))
    module_issues, module_paths = validate_module_map(repository_root)
    issues.extend(module_issues)
    issues.extend(validate_scenario_registry(repository_root, module_paths))
    scenario_registry = repository_root / SCENARIO_REGISTRY
    if scenario_registry.is_file():
        try:
            scenario_content = scenario_registry.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            scenario_content = ""
        if HUMAN_CONFIRMATION_SCENARIO in scenario_content:
            issues.extend(validate_human_confirmation_contract(repository_root))
    issues.extend(validate_readme_links(repository_root))
    if (repository_root / "harness").is_dir():
        issues.extend(validate_harness_entries(repository_root))
    if (repository_root / "skills/superCoder/agents").exists():
        issues.extend(validate_openai_metadata(repository_root))
    issues = sorted(issues, key=lambda item: (item["code"], item["path"], item["message"]))
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PASS" if not issues else "FAIL",
        "issue_count": len(issues),
        "issues": issues,
    }


def render_text(result: dict[str, Any]) -> str:
    lines = [f"package validation: {result['status']} ({result['issue_count']} issues)"]
    for item in result["issues"]:
        lines.append(f"{item['code']} {item['path']}: {item['message']}")
    return "\n".join(lines)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="repository root")
    parser.add_argument("--format", choices=("json", "text"), default="text")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    result = validate_repository(Path(args.root))
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    else:
        print(render_text(result))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
