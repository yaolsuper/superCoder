#!/usr/bin/env python3
"""Execute the canonical knowledge CLI through a named harness adapter."""
from __future__ import annotations
import argparse, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]; CLI=ROOT/"skills/superCoder/scripts/coder_knowledge.py"
ADAPTERS={"app-agent":"1","opencode":"1"}
def run(adapter:str,arguments:list[str]):
    if adapter not in ADAPTERS: raise ValueError(f"unsupported adapter: {adapter}")
    return subprocess.run([sys.executable,"-B",str(CLI),*arguments],cwd=ROOT,capture_output=True,text=True,timeout=30)
def main(argv=None):
    parser=argparse.ArgumentParser(); parser.add_argument("--adapter",choices=sorted(ADAPTERS),required=True); parser.add_argument("arguments",nargs=argparse.REMAINDER); args=parser.parse_args(argv)
    arguments=args.arguments[1:] if args.arguments[:1]==["--"] else args.arguments; result=run(args.adapter,arguments)
    sys.stdout.write(result.stdout); sys.stderr.write(result.stderr); return result.returncode
if __name__=="__main__": sys.exit(main())
