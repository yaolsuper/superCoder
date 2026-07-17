#!/usr/bin/env python3
"""Compare canonical JSON, exit code, error code, and disclosure scope across adapters."""
from __future__ import annotations
import argparse, json, sys
from adapter_runner import run
def compare(adapters,arguments):
    results=[]
    for adapter in adapters:
        proc=run(adapter,arguments)
        try: body=json.loads(proc.stdout)
        except json.JSONDecodeError: body=None
        results.append({"adapter":adapter,"exit_code":proc.returncode,"body":body,"raw":proc.stdout})
    base=results[0]; differences=[]
    for item in results[1:]:
        if item["exit_code"]!=base["exit_code"]: differences.append("EXIT_CODE_DRIFT")
        if item["body"]!=base["body"]: differences.append("JSON_SHAPE_DRIFT")
    return {"contract_version":"supercoder.adapter-contract/v1","adapters":adapters,"semantic_equal":not differences,"differences":sorted(set(differences))}
def main(argv=None):
    p=argparse.ArgumentParser(); p.add_argument("--adapter",action="append",required=True); p.add_argument("arguments",nargs=argparse.REMAINDER); a=p.parse_args(argv); arguments=a.arguments[1:] if a.arguments[:1]==["--"] else a.arguments
    result=compare(a.adapter,arguments); print(json.dumps(result,sort_keys=True)); return 0 if result["semantic_equal"] else 1
if __name__=="__main__": sys.exit(main())
