from __future__ import annotations
import hashlib, json, re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from validate_trace_contract import validate_manifest

MANIFEST_RE = re.compile(r"<!-- sc:manifest -->\s*```json\s*(.*?)\s*```\s*<!-- /sc:manifest -->", re.S)
SECTION_RE = re.compile(r'<!-- sc:section id="([a-z0-9][a-z0-9._-]*)" digest="([0-9a-f]{64})" -->\n(.*?)<!-- /sc:section -->', re.S)

class KnowledgeError(Exception):
    def __init__(self, code: str, message: str): super().__init__(message); self.code = code

@dataclass
class Card:
    path: Path
    manifest: dict[str, Any]
    sections: dict[str, dict[str, str]]

def inside(repo: Path, path: Path) -> bool:
    try: path.resolve().relative_to(repo.resolve()); return True
    except ValueError: return False

def parse_card(path: Path) -> Card:
    text = path.read_text(encoding="utf-8")
    if text.count("<!-- sc:manifest -->") != 1 or text.count("<!-- /sc:manifest -->") != 1:
        raise KnowledgeError("PARSE_FAILURE", "manifest markers must be balanced and unique")
    if text.count("<!-- sc:section ") != text.count("<!-- /sc:section -->"):
        raise KnowledgeError("SECTION_UNBALANCED", "section markers must be balanced")
    matches = MANIFEST_RE.findall(text)
    if len(matches) != 1: raise KnowledgeError("PARSE_FAILURE", "exactly one manifest block is required")
    try: manifest = json.loads(matches[0])
    except json.JSONDecodeError as exc: raise KnowledgeError("PARSE_FAILURE", str(exc)) from exc
    sections: dict[str, dict[str, str]] = {}
    for sid, declared, content in SECTION_RE.findall(text):
        if sid in sections: raise KnowledgeError("SECTION_DUPLICATE", sid)
        actual = hashlib.sha256(content.encode("utf-8")).hexdigest()
        if actual != declared: raise KnowledgeError("SECTION_HASH_DRIFT", sid)
        sections[sid] = {"id":sid,"digest":actual,"content":content}
    declared_ids = {item.get("id") for item in manifest.get("sections", [])}
    if declared_ids != set(sections): raise KnowledgeError("SECTION_UNBALANCED", "manifest and Markdown sections differ")
    for item in manifest.get("sections", []):
        if sections[item["id"]]["digest"] != item.get("digest"): raise KnowledgeError("SECTION_HASH_DRIFT", item["id"])
    return Card(path, manifest, sections)

def locate(repo: Path, *, project_id: str | None=None, requirement_id: str | None=None, module_id: str | None=None) -> Path:
    repo = repo.resolve()
    if module_id:
        candidates = [repo / ".coder/_knowledge/product-modules" / f"{module_id}.md"]
    elif project_id:
        candidates = [repo / ".coder" / project_id / "requirement-knowledge-card.md"]
    else:
        candidates = sorted(repo.glob(".coder/*/requirement-knowledge-card.md"))
    candidates = [p for p in candidates if p.is_file() and inside(repo, p)]
    if requirement_id:
        candidates = [p for p in candidates if parse_card(p).manifest.get("resource", {}).get("id") == requirement_id]
    if not candidates: raise KnowledgeError("NOT_FOUND", "canonical resource was not found")
    if len(candidates) != 1: raise KnowledgeError("AMBIGUOUS", "selector matched multiple canonical resources")
    return candidates[0]

def validate_card(card: Card, *, module: bool=False) -> list[dict[str, str]]:
    issues = list(validate_manifest(card.manifest)["issues"])
    resource = card.manifest.get("resource", {})
    expected = "Module" if module else "Requirement"
    if resource.get("type") != expected: issues.append({"code":"RESOURCE_KIND_INVALID","path":"$.resource.type","message":f"expected {expected}"})
    if module:
        data = card.manifest.get("module")
        if not isinstance(data, dict) or data.get("module_id") != resource.get("id"):
            issues.append({"code":"MODULE_INVALID","path":"$.module","message":"module metadata must match resource"})
        elif not isinstance(data.get("aliases", []), list) or not isinstance(data.get("capabilities", []), list) or not isinstance(data.get("code_bindings", []), list):
            issues.append({"code":"MODULE_INVALID","path":"$.module","message":"aliases/capabilities/code_bindings must be arrays"})
        elif data.get("parent_ref") == resource.get("ref"):
            issues.append({"code":"MODULE_CONFLICT","path":"$.module.parent_ref","message":"module cannot parent itself"})
        if resource.get("status") == "ACTIVE" and not card.manifest.get("governance", {}).get("approved_by"):
            issues.append({"code":"OWNERSHIP_VIOLATION","path":"$.governance.approved_by","message":"ACTIVE module requires explicit approval"})
    return sorted(issues, key=lambda x:(x["path"],x["code"]))
