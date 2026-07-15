#!/usr/bin/env python3
"""Validate a superCoder trace manifest using only the Python standard library."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "supercoder.trace/v1"
REF_RE = re.compile(r"^sc://([a-z0-9][a-z0-9.-]*)/([a-z0-9][a-z0-9.-]*)/([a-z][a-z0-9-]*)/([a-z0-9][a-z0-9._-]*)$")
DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")
TYPES = {"Requirement","Module","Capability","Claim","Argument","Evidence","Change","Risk","Recommendation","Activity","Agent","Artifact","Validation"}
TYPE_PATH = {value: re.sub(r"(?<!^)(?=[A-Z])", "-", value).lower() for value in TYPES}
STATES = {
    "Requirement":{"DISCOVERED","ANALYZED","PLANNED","IMPLEMENTED","VERIFIED","ACCEPTED","SUPERSEDED"},
    "Module":{"CANDIDATE","ACTIVE","DEPRECATED","RETIRED"},
    "Risk":{"OPEN","MITIGATED","ACCEPTED","CLOSED"},
    "Recommendation":{"PROPOSED","ACCEPTED","REJECTED","IMPLEMENTED"},
    "Change":{"EXPECTED","ACTUAL","REVERTED"},
    "Validation":{"PENDING","PASSED","FAILED","STALE"},
}
for _type in TYPES - STATES.keys():
    STATES[_type] = {"ACTIVE","INACTIVE"} if _type != "Activity" else {"PLANNED","RUNNING","COMPLETED","FAILED"}
OWNERS = {
    "Requirement":{"analysis","review"}, "Claim":{"analysis","review"}, "Argument":{"analysis","review"}, "Evidence":{"analysis","review"},
    "Module":{"product-module-registry"}, "Capability":{"product-module-registry"}, "Change":{"plan","execution"},
    "Risk":{"decision"}, "Recommendation":{"decision"}, "Validation":{"validation-record"},
    "Activity":{"execution"}, "Agent":{"execution"}, "Artifact":{"execution"},
}
RELATIONS = {
    "REQUIREMENT_HAS_CLAIM","CLAIM_SUPPORTED_BY_ARGUMENT","ARGUMENT_SUPPORTED_BY_EVIDENCE",
    "REQUIREMENT_ALLOCATED_TO_MODULE","MODULE_HAS_CAPABILITY","CHANGE_SATISFIES_REQUIREMENT",
    "CHANGE_TOUCHES_MODULE","VALIDATION_VERIFIES_CHANGE","VALIDATION_VERIFIES_CLAIM","VALIDATION_VERIFIES_MODULE",
    "RISK_AFFECTS_RESOURCE","RECOMMENDATION_TARGETS_RESOURCE","ACTIVITY_USED","ACTIVITY_GENERATED","ACTIVITY_ASSOCIATED_WITH",
    "DEPENDS_ON","EXTENDS","OVERLAPS","CONFLICTS_WITH","SUPERSEDES","REGRESSION_RISK",
}

def issue(code: str, path: str, message: str) -> dict[str, str]:
    return {"code": code, "path": path, "message": message}

def validate_manifest(data: Any) -> dict[str, Any]:
    issues: list[dict[str, str]] = []
    if not isinstance(data, dict):
        return {"schema_version":SCHEMA_VERSION,"status":"FAIL","issues":[issue("MANIFEST_INVALID","$","manifest must be an object")]}
    if data.get("schema_version") != SCHEMA_VERSION:
        issues.append(issue("SCHEMA_UNSUPPORTED","$.schema_version",f"expected {SCHEMA_VERSION}"))
    repo, project = data.get("repository_id"), data.get("development_project_id")
    if not repo:
        issues.append(issue("REPOSITORY_ID_MISSING","$.repository_id","repository_id is required for canonical refs"))
    if not project:
        issues.append(issue("PROJECT_ID_MISSING","$.development_project_id","development_project_id is required"))
    resources = [data.get("resource")] + list(data.get("entities") or [])
    seen_ids: set[tuple[str, str]] = set()
    refs: set[str] = set()
    for index, resource in enumerate(resources):
        path = "$.resource" if index == 0 else f"$.entities[{index-1}]"
        if not isinstance(resource, dict):
            issues.append(issue("RESOURCE_INVALID",path,"resource must be an object")); continue
        rtype, rid, ref = resource.get("type"), resource.get("id"), resource.get("ref")
        if rtype not in TYPES:
            issues.append(issue("TYPE_UNKNOWN",f"{path}.type","unknown resource type"))
        key = (str(rtype), str(rid))
        if key in seen_ids:
            issues.append(issue("ID_DUPLICATE",f"{path}.id","id must be unique within its type"))
        seen_ids.add(key)
        match = REF_RE.fullmatch(str(ref or ""))
        if not match or (rtype in TYPE_PATH and match and match.group(3) != TYPE_PATH[rtype]) or (match and (match.group(1) != repo or match.group(2) != project or match.group(4) != rid)):
            issues.append(issue("REF_INVALID",f"{path}.ref","ref must match manifest identity and resource type"))
        else:
            if ref in refs: issues.append(issue("ID_DUPLICATE",f"{path}.ref","ref must be unique"))
            refs.add(ref)
        if resource.get("status") not in STATES.get(rtype, set()):
            issues.append(issue("STATE_INVALID",f"{path}.status","status is not allowed for resource type"))
        if resource.get("owner") not in OWNERS.get(rtype, set()):
            issues.append(issue("OWNERSHIP_VIOLATION",f"{path}.owner","owner is not authoritative for resource type"))
        if not isinstance(resource.get("revision"), int) or resource.get("revision", 0) < 1:
            issues.append(issue("REVISION_INVALID",f"{path}.revision","revision must be a positive integer"))
        if not DIGEST_RE.fullmatch(str(resource.get("digest") or "")):
            issues.append(issue("DIGEST_INVALID",f"{path}.digest","digest must be lowercase sha256"))
    relations = data.get("relations") or []
    outgoing: dict[tuple[str, str], int] = {}
    rel_ids: set[str] = set()
    for index, relation in enumerate(relations):
        path = f"$.relations[{index}]"
        if not isinstance(relation, dict): issues.append(issue("RELATION_INVALID",path,"relation must be an object")); continue
        rel_id, rel_type = relation.get("id"), relation.get("type")
        if rel_id in rel_ids: issues.append(issue("ID_DUPLICATE",f"{path}.id","relation id must be unique"))
        rel_ids.add(rel_id)
        if rel_type not in RELATIONS: issues.append(issue("RELATION_UNKNOWN",f"{path}.type","relation type is not registered"))
        for field in ("source_ref","target_ref"):
            value = relation.get(field)
            if not REF_RE.fullmatch(str(value or "")): issues.append(issue("REF_INVALID",f"{path}.{field}","relation ref is invalid"))
            elif value not in refs: issues.append(issue("REF_UNRESOLVED",f"{path}.{field}","relation ref does not resolve in manifest"))
        outgoing[(str(relation.get("source_ref")), str(rel_type))] = outgoing.get((str(relation.get("source_ref")), str(rel_type)), 0) + 1
    for resource in resources:
        if not isinstance(resource, dict): continue
        required = {"Claim":"CLAIM_SUPPORTED_BY_ARGUMENT","Argument":"ARGUMENT_SUPPORTED_BY_EVIDENCE"}.get(resource.get("type"))
        if required and outgoing.get((str(resource.get("ref")), required), 0) < 1:
            issues.append(issue("CARDINALITY_VIOLATION",f"$.relations",f"{resource.get('type')} {resource.get('id')} requires {required}"))
    section_ids: set[str] = set()
    for index, section in enumerate(data.get("sections") or []):
        path = f"$.sections[{index}]"; sid = section.get("id") if isinstance(section, dict) else None
        if sid in section_ids: issues.append(issue("SECTION_DUPLICATE",f"{path}.id","section id must be unique"))
        section_ids.add(sid)
        if not isinstance(section, dict) or not DIGEST_RE.fullmatch(str(section.get("digest") or "")):
            issues.append(issue("SECTION_HASH_DRIFT",f"{path}.digest","section digest must be lowercase sha256"))
    issues.sort(key=lambda item: (item["path"], item["code"], item["message"]))
    return {"schema_version":SCHEMA_VERSION,"status":"PASS" if not issues else "FAIL","issues":issues}

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path"); parser.add_argument("--kind", default="manifest"); parser.add_argument("--format", choices=("json","text"), default="text")
    args = parser.parse_args(argv); path = Path(args.path)
    if path.is_dir(): path = path / "manifest.json"
    try: data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        result = {"schema_version":SCHEMA_VERSION,"status":"FAIL","issues":[issue("PARSE_ERROR",str(path),str(exc))]}
    else: result = validate_manifest(data)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) if args.format == "json" else f"trace contract: {result['status']} ({len(result['issues'])} issues)")
    return 0 if result["status"] == "PASS" else 1

if __name__ == "__main__": sys.exit(main())
