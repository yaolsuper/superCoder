#!/usr/bin/env python3
"""Bounded CLI for superCoder requirement cards, product modules, and derived indexes."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from knowledge.core import KnowledgeError, locate, parse_card, validate_card
from knowledge.index import load as load_index, rebuild as rebuild_index, related as related_rows
from knowledge.materialize import materialize

SCHEMA = "supercoder.knowledge-cli/v1"
EXIT = {"NOT_FOUND":3,"AMBIGUOUS":4,"INVALID_SCOPE":5,"SECTION_HASH_DRIFT":6,"PARSE_FAILURE":7}

def envelope(command: str, status: str, data=None, issues=None):
    return {"schema_version":SCHEMA,"command":command,"status":status,"data":data,"issues":issues or []}

def selector(args):
    return {"project_id":getattr(args,"project_id",None),"requirement_id":getattr(args,"requirement_id",None),"module_id":getattr(args,"module_id",None)}

def execute(args):
    repo = Path(args.repo).resolve()
    if args.command == "materialize": return materialize(repo,args.project_id,args.dry_run)
    if args.command == "rebuild-index": return rebuild_index(repo)
    if args.command == "validate-index":
        meta,_=load_index(repo); return {"fresh":True,"metadata":meta}
    if args.command in ("find","related","impact","tree"):
        meta,rows=load_index(repo)
        if args.command=="find":
            needle=args.module; refs={m["ref"] for m in rows["modules"] if needle==m["module_id"] or needle in m["aliases"]}
            if not refs: raise KnowledgeError("MODULE_NOT_FOUND",needle)
            if len(refs)>1: raise KnowledgeError("AMBIGUOUS",needle)
            return {"requirements":[r for r in rows["requirements"] if refs.intersection(r["module_refs"])][:args.limit]}
        if args.command=="related": return {"relations":related_rows(rows,args.ref,args.limit)}
        if args.command=="impact":
            seen={args.ref}; frontier=[args.ref]; edges=[]
            for _ in range(args.depth):
                nxt=[]
                for ref in frontier:
                    for rel in related_rows(rows,ref,args.limit):
                        if rel not in edges: edges.append(rel)
                        other=rel["target_ref"] if rel["source_ref"]==ref else rel["source_ref"]
                        if other not in seen and len(seen)<args.limit: seen.add(other); nxt.append(other)
                frontier=nxt
            return {"nodes":sorted(seen),"relations":edges[:args.limit],"truncated":len(seen)>=args.limit}
        root=next((m for m in rows["modules"] if m["module_id"]==args.module),None)
        if not root: raise KnowledgeError("MODULE_NOT_FOUND",args.module)
        def node(item,trail):
            if item["ref"] in trail: return {"ref":item["ref"],"cycle":True}
            children=[node(m,trail|{item["ref"]}) for m in rows["modules"] if m.get("parent_ref")==item["ref"]]
            return {"ref":item["ref"],"module_id":item["module_id"],"status":item["status"],"children":children}
        return node(root,set())
    path = locate(repo, **selector(args)); card = parse_card(path)
    relpath = path.relative_to(repo).as_posix()
    if args.command == "locate": return {"path":relpath,"ref":card.manifest["resource"]["ref"]}
    if args.command == "metadata":
        return {key:card.manifest.get(key) for key in ("schema_version","repository_id","development_project_id","resource","sections")}
    if args.command == "section":
        if args.section not in card.sections: raise KnowledgeError("SECTION_NOT_FOUND", args.section)
        return card.sections[args.section]
    if args.command == "entity":
        matches = [x for x in [card.manifest.get("resource")]+card.manifest.get("entities",[]) if x and x.get("id") == args.entity_id]
        if not matches: raise KnowledgeError("ENTITY_NOT_FOUND", args.entity_id)
        if len(matches)>1: raise KnowledgeError("AMBIGUOUS", args.entity_id)
        ref=matches[0]["ref"]; relations=[r for r in card.manifest.get("relations",[]) if ref in (r.get("source_ref"),r.get("target_ref"))]
        return {"entity":matches[0],"relations":relations}
    if args.command in ("validate-card","validate-module"):
        issues=validate_card(card,module=args.command=="validate-module")
        if issues: raise KnowledgeError(issues[0]["code"], json.dumps(issues,ensure_ascii=False))
        return {"path":relpath,"resource":card.manifest["resource"],"valid":True}
    raise KnowledgeError("COMMAND_UNSUPPORTED", args.command)

def add_selector(parser):
    parser.add_argument("--repo", required=True); parser.add_argument("--project-id"); parser.add_argument("--requirement-id"); parser.add_argument("--module-id")

def parse_args(argv=None):
    parser=argparse.ArgumentParser(description=__doc__); sub=parser.add_subparsers(dest="command",required=True)
    for name in ("locate","metadata","validate-card","validate-module"):
        add_selector(sub.add_parser(name))
    p=sub.add_parser("section"); add_selector(p); p.add_argument("--section",required=True)
    p=sub.add_parser("entity"); add_selector(p); p.add_argument("--entity-id",required=True)
    for name in ("rebuild-index","validate-index"):
        p=sub.add_parser(name); p.add_argument("--repo",required=True)
    p=sub.add_parser("find"); p.add_argument("--repo",required=True); p.add_argument("--module",required=True); p.add_argument("--limit",type=int,default=50)
    p=sub.add_parser("related"); p.add_argument("--repo",required=True); p.add_argument("--ref",required=True); p.add_argument("--limit",type=int,default=50)
    p=sub.add_parser("impact"); p.add_argument("--repo",required=True); p.add_argument("--ref",required=True); p.add_argument("--depth",type=int,default=2); p.add_argument("--limit",type=int,default=100)
    p=sub.add_parser("tree"); p.add_argument("--repo",required=True); p.add_argument("--module",required=True)
    p=sub.add_parser("materialize"); p.add_argument("--repo",required=True); p.add_argument("--project-id",required=True); p.add_argument("--dry-run",action="store_true")
    return parser.parse_args(argv)

def main(argv=None):
    args=parse_args(argv)
    try: body=envelope(args.command,"PASS",execute(args)); code=0
    except (KnowledgeError,OSError) as exc:
        error=getattr(exc,"code","IO_ERROR"); body=envelope(args.command,"FAIL",issues=[{"code":error,"message":str(exc)}]); code=EXIT.get(error,5)
    print(json.dumps(body,ensure_ascii=False,sort_keys=True)); return code

if __name__ == "__main__": sys.exit(main())
