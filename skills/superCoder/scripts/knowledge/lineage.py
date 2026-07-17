from __future__ import annotations
from typing import Any

def validate_lineage(operations: list[dict[str,Any]], validations: list[dict[str,Any]]) -> list[dict[str,str]]:
    issues=[]; ids=set(); output_refs=set()
    for i,event in enumerate(operations):
        path=f"$.operations[{i}]"; eid=event.get("event_id")
        if eid in ids: issues.append({"code":"EVENT_ID_DUPLICATE","path":path+".event_id","message":"event id is append-only and unique"})
        parent=event.get("parent_event_id")
        if parent and parent not in ids: issues.append({"code":"PARENT_UNRESOLVED","path":path+".parent_event_id","message":"parent must precede child"})
        retry=event.get("retry_of")
        if retry and retry not in ids: issues.append({"code":"RETRY_INVALID","path":path+".retry_of","message":"retry target must precede retry"})
        ids.add(eid)
        producer=event.get("producer") or {}
        if any(not producer.get(k) or producer.get(k)=="unknown" for k in ("name","version","harness","model")): issues.append({"code":"PRODUCER_INVALID","path":path+".producer","message":"producer attribution is required"})
        for side in ("inputs","outputs"):
            for j,item in enumerate(event.get(side,[])):
                if not item.get("ref") or not isinstance(item.get("revision"),int) or len(str(item.get("digest","")))!=64: issues.append({"code":"VERSIONED_IO_INVALID","path":f"{path}.{side}[{j}]","message":"ref/revision/digest required"})
                if side=="outputs" and item.get("ref"): output_refs.add(item["ref"])
    for i,val in enumerate(validations):
        path=f"$.validations[{i}]"
        if val.get("result") not in ("PASSED","FAILED"): issues.append({"code":"VALIDATION_NOT_EXECUTED","path":path+".result","message":"NOT_RUN/unknown cannot pass"})
        if not val.get("evidence_ref"): issues.append({"code":"EVIDENCE_MISSING","path":path+".evidence_ref","message":"validation evidence required"})
        for ref in val.get("target_refs",[]):
            if ref not in output_refs: issues.append({"code":"VALIDATION_TARGET_UNRESOLVED","path":path+".target_refs","message":"target must resolve to actual output"})
    return sorted(issues,key=lambda x:(x["path"],x["code"]))
