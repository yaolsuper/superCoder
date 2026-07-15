from __future__ import annotations
import hashlib, json, os, shutil, tempfile
from pathlib import Path
from typing import Any
from knowledge.core import KnowledgeError, inside, parse_card, validate_card

INDEX_SCHEMA="supercoder.knowledge-index/v1"

def canonical(value: Any) -> str: return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"))
def sources(repo: Path) -> list[Path]:
    paths=list(repo.glob(".coder/*/requirement-knowledge-card.md"))+list(repo.glob(".coder/_knowledge/product-modules/*.md"))
    return sorted(p for p in paths if p.is_file() and inside(repo,p))
def source_digest(repo: Path, paths: list[Path]) -> str:
    h=hashlib.sha256()
    for p in paths: h.update(p.relative_to(repo).as_posix().encode()); h.update(b"\0"); h.update(p.read_bytes()); h.update(b"\0")
    return h.hexdigest()
def build_rows(repo: Path):
    reqs=[]; modules=[]; relations=[]; paths=sources(repo)
    for path in paths:
        card=parse_card(path); issues=validate_card(card,module="product-modules" in path.parts)
        if issues: raise KnowledgeError("SOURCE_INVALID",canonical(issues))
        m=card.manifest; r=m["resource"]; digest=hashlib.sha256(path.read_bytes()).hexdigest()
        if r["type"]=="Requirement":
            module_refs=sorted(x["target_ref"] for x in m.get("relations",[]) if x["type"]=="REQUIREMENT_ALLOCATED_TO_MODULE" and x["source_ref"]==r["ref"])
            reqs.append({"ref":r["ref"],"project_id":m["development_project_id"],"requirement_id":r["id"],"module_refs":module_refs,"status":r["status"],"source_digest":digest,"source_path":path.relative_to(repo).as_posix()})
        elif r["type"]=="Module":
            md=m.get("module",{}); modules.append({"ref":r["ref"],"module_id":r["id"],"parent_ref":md.get("parent_ref"),"aliases":sorted(md.get("aliases",[])),"status":r["status"],"revision":r["revision"],"source_digest":digest,"source_path":path.relative_to(repo).as_posix()})
        for rel in m.get("relations",[]): relations.append({**rel,"source_digest":digest})
    ids=[x["module_id"] for x in modules]
    if len(ids)!=len(set(ids)): raise KnowledgeError("MODULE_CONFLICT","duplicate module id")
    refs={x["ref"] for x in modules}; aliases={}
    for module in modules:
        if module.get("parent_ref") and module["parent_ref"] not in refs: raise KnowledgeError("MODULE_CONFLICT","parent ref is unresolved")
        for alias in module["aliases"]:
            if alias in aliases and aliases[alias] != module["ref"]: raise KnowledgeError("MODULE_CONFLICT","module alias is ambiguous")
            aliases[alias]=module["ref"]
    parents={x["ref"]:x.get("parent_ref") for x in modules}
    for ref in parents:
        seen=set(); current=ref
        while current:
            if current in seen: raise KnowledgeError("MODULE_CONFLICT","module parent cycle")
            seen.add(current); current=parents.get(current)
    return sorted(reqs,key=lambda x:x["ref"]),sorted(modules,key=lambda x:x["ref"]),sorted(relations,key=lambda x:(x["id"],x["source_ref"],x["target_ref"])),paths
def rebuild(repo: Path):
    repo=repo.resolve(); reqs,mods,rels,paths=build_rows(repo); parent=repo/".coder"; parent.mkdir(exist_ok=True)
    tmp=Path(tempfile.mkdtemp(prefix=".index-",dir=parent)); target=parent/"_index"; backup=parent/".index-backup"
    try:
        for name,rows in (("requirements.jsonl",reqs),("modules.jsonl",mods),("relations.jsonl",rels)):
            (tmp/name).write_text("".join(canonical(row)+"\n" for row in rows),encoding="utf-8")
        meta={"schema_version":INDEX_SCHEMA,"source_set_digest":source_digest(repo,paths),"counts":{"requirements":len(reqs),"modules":len(mods),"relations":len(rels)}}
        (tmp/"metadata.json").write_text(canonical(meta)+"\n",encoding="utf-8")
        if backup.exists(): shutil.rmtree(backup)
        if target.exists(): os.replace(target,backup)
        try: os.replace(tmp,target)
        except Exception:
            if backup.exists(): os.replace(backup,target)
            raise
        if backup.exists(): shutil.rmtree(backup)
        return meta
    finally:
        if tmp.exists(): shutil.rmtree(tmp)
def load(repo: Path):
    root=repo/".coder/_index"
    try:
        meta=json.loads((root/"metadata.json").read_text())
        rows={name:[json.loads(line) for line in (root/f"{name}.jsonl").read_text().splitlines() if line] for name in ("requirements","modules","relations")}
    except OSError as exc: raise KnowledgeError("INDEX_MISSING",str(exc)) from exc
    except json.JSONDecodeError as exc: raise KnowledgeError("INDEX_INVALID",str(exc)) from exc
    current=source_digest(repo,sources(repo))
    if meta.get("source_set_digest")!=current: raise KnowledgeError("INDEX_STALE","source set changed; rebuild required")
    return meta,rows
def related(rows,ref:str,limit:int=50): return [r for r in rows["relations"] if ref in (r["source_ref"],r["target_ref"])][:limit]
