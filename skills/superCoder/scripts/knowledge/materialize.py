from __future__ import annotations
import hashlib, json, os, re, tempfile
from pathlib import Path
from typing import Any
from knowledge.core import KnowledgeError, MANIFEST_RE, locate, parse_card, validate_card
from knowledge.index import rebuild
from knowledge.lineage import validate_lineage

def canonical(value:Any)->str: return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"))
def governance(data):
    for risk in data.get("risks",[]):
        if risk.get("state")=="ACCEPTED" and not risk.get("decision_ref"): raise KnowledgeError("RISK_ACCEPTANCE_MISSING",risk.get("risk_id","risk"))
    for rec in data.get("recommendations",[]):
        if rec.get("type") not in ("PRODUCT","ENGINEERING"): raise KnowledgeError("RECOMMENDATION_TYPE_INVALID",rec.get("recommendation_id","recommendation"))
        if rec.get("state") in ("ACCEPTED","IMPLEMENTED") and not rec.get("decision_ref"): raise KnowledgeError("RECOMMENDATION_ELEVATION_INVALID",rec.get("recommendation_id","recommendation"))
    for module in data.get("module_proposals",[]):
        if module.get("status")=="ACTIVE" and not module.get("review_evidence_ref"): raise KnowledgeError("GOVERNANCE_EVIDENCE_MISSING",module.get("module_id","module"))
def validate_summary(data):
    forbidden=re.compile(r"(?:[/\\]|\b(?:class|method|command|MR-\d+|CP[0-5]|\.py|\.java|src)\b)",re.I)
    for field in ("why","who","what"):
        value=data.get(field)
        if not isinstance(value,str) or not value.strip(): raise KnowledgeError("DELIVERY_SUMMARY_DRIFT",f"{field} is required")
        if forbidden.search(value): raise KnowledgeError("DELIVERY_SUMMARY_DRIFT",f"{field} contains implementation detail")
def propose(repo:Path,project_id:str):
    card=parse_card(locate(repo,project_id=project_id)); issues=validate_card(card)
    if issues: raise KnowledgeError("CARD_DRIFT",canonical(issues))
    input_path=repo/".coder"/project_id/"records/completion-input.json"
    try: data=json.loads(input_path.read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as exc: raise KnowledgeError("LEDGER_INCOMPLETE",str(exc)) from exc
    lineage=validate_lineage(data.get("operations",[]),data.get("validations",[]))
    if lineage: raise KnowledgeError(lineage[0]["code"],canonical(lineage))
    governance(data)
    validate_summary(data)
    reconciliations=[]
    for expected in data.get("expected_changes",[]):
        actual=expected.get("actual_refs",[]); result="MATCHED" if actual else "UNRESOLVED"
        reconciliations.append({"expected_ref":expected.get("ref"),"actual_refs":actual,"result":result,"evidence_refs":expected.get("evidence_refs",[])})
    if any(x["result"]=="UNRESOLVED" for x in reconciliations): raise KnowledgeError("EXPECTED_CHANGE_UNRESOLVED","all expected changes require actual evidence")
    m=card.manifest; base=f"sc://{m['repository_id']}/{m['development_project_id']}"; requirement=m["resource"]["ref"]
    risk_refs=sorted(f"{base}/risk/{x['risk_id']}" for x in data.get("risks",[])); recommendation_refs=sorted(f"{base}/recommendation/{x['recommendation_id']}" for x in data.get("recommendations",[])); actual_refs=sorted(x["ref"] for x in data.get("actual_changes",[])); validation_refs=sorted(x["ref"] for x in data.get("validations",[]))
    relations=list(m.get("relations",[]))
    relations += [{"id":f"final-change-{i}","type":"CHANGE_SATISFIES_REQUIREMENT","source_ref":ref,"target_ref":requirement,"state":"ACTIVE"} for i,ref in enumerate(actual_refs,1)]
    for i,val in enumerate(data.get("validations",[]),1):
        relations += [{"id":f"final-validation-{i}-{j}","type":"VALIDATION_VERIFIES_CHANGE","source_ref":val["ref"],"target_ref":target,"state":"ACTIVE"} for j,target in enumerate(val.get("target_refs",[]),1)]
    relations += [{"id":f"final-risk-{i}","type":"RISK_AFFECTS_RESOURCE","source_ref":ref,"target_ref":requirement,"state":"ACTIVE"} for i,ref in enumerate(risk_refs,1)]
    module_refs=sorted(x["target_ref"] for x in m.get("relations",[]) if x["type"]=="REQUIREMENT_ALLOCATED_TO_MODULE"); rec_target=module_refs[0] if module_refs else requirement
    relations += [{"id":f"final-recommendation-{i}","type":"RECOMMENDATION_TARGETS_RESOURCE","source_ref":ref,"target_ref":rec_target,"state":"ACTIVE"} for i,ref in enumerate(recommendation_refs,1)]
    graph={"requirement_ref":requirement,"claim_refs":sorted(x.get("ref") for x in data.get("claims",[]) if x.get("ref")),"change_refs":actual_refs,"module_refs":module_refs,"validation_refs":validation_refs,"risk_refs":risk_refs,"recommendation_refs":recommendation_refs,"relations":relations,"module_proposals":[{**x,"status":x.get("status","CANDIDATE")} for x in data.get("module_proposals",[])],"status":"ACCEPTED" if data.get("validations") and all(x["result"]=="PASSED" for x in data["validations"]) else "VERIFYING","source_digests":sorted([hashlib.sha256(card.path.read_bytes()).hexdigest(),hashlib.sha256(input_path.read_bytes()).hexdigest()])}
    return card,data,{"graph":graph,"reconciliation":reconciliations}
def render(card,graph):
    text=card.path.read_text(encoding="utf-8"); content=canonical(graph)+"\n"; digest=hashlib.sha256(content.encode()).hexdigest(); marker=f'<!-- sc:section id="final-graph" digest="{digest}" -->\n{content}<!-- /sc:section -->'
    existing=re.compile(r'<!-- sc:section id="final-graph" digest="[0-9a-f]{64}" -->\n.*?<!-- /sc:section -->',re.S); text=existing.sub(marker,text) if existing.search(text) else text.rstrip()+"\n\n"+marker+"\n"
    manifest=dict(card.manifest); manifest["resource"]=dict(manifest["resource"]); manifest["resource"]["status"]="ACCEPTED"; manifest["sections"]=[x for x in manifest.get("sections",[]) if x.get("id")!="final-graph"]+[{"id":"final-graph","digest":digest}]
    replacement="<!-- sc:manifest -->\n```json\n"+canonical(manifest)+"\n```\n<!-- /sc:manifest -->"; return MANIFEST_RE.sub(replacement,text)
def atomic_write(path:Path,text:str):
    fd,name=tempfile.mkstemp(prefix=".knowledge-",dir=path.parent); os.close(fd); tmp=Path(name)
    try: tmp.write_text(text,encoding="utf-8"); os.replace(tmp,path)
    finally:
        if tmp.exists(): tmp.unlink()
def materialize(repo:Path,project_id:str,dry_run:bool=False):
    card,data,result=propose(repo,project_id)
    if dry_run:return result
    original=card.path.read_bytes(); summary=repo/".coder"/project_id/"requirement-delivery-summary.md"; old_summary=summary.read_bytes() if summary.exists() else None
    try:
        atomic_write(card.path,render(card,result["graph"])); parsed=parse_card(card.path); issues=validate_card(parsed)
        if issues: raise KnowledgeError("CARD_DRIFT",canonical(issues))
        body=f"# 需求最终落地摘要\n\n## Why\n\n{data['why']}\n\n## Who\n\n{data['who']}\n\n## What\n\n{data['what']}\n"; atomic_write(summary,body); rebuild(repo)
    except Exception:
        card.path.write_bytes(original)
        if old_summary is None and summary.exists(): summary.unlink()
        elif old_summary is not None: summary.write_bytes(old_summary)
        raise
    return result
