from __future__ import annotations
import copy, json, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]; CLI=ROOT/"skills/superCoder/scripts/coder_knowledge.py"; FIXTURE=ROOT/"tests/skill-behavior/fixtures/completion-materialization/valid-repo"
class CompletionTests(unittest.TestCase):
    def setUp(self): self.tmp=tempfile.TemporaryDirectory(); self.repo=Path(self.tmp.name)/"repo"; shutil.copytree(FIXTURE,self.repo)
    def tearDown(self): self.tmp.cleanup()
    def run_cli(self,*extra):
        result=subprocess.run([sys.executable,"-B",str(CLI),"materialize","--repo",str(self.repo),"--project-id","demo-20260715",*extra],capture_output=True,text=True)
        return result,json.loads(result.stdout)
    def test_dry_run_is_idempotent_and_has_actual_evidence(self):
        a,b=self.run_cli("--dry-run"),self.run_cli("--dry-run"); self.assertEqual(0,a[0].returncode); self.assertEqual(a[1]["data"],b[1]["data"])
        self.assertEqual("ACCEPTED",a[1]["data"]["graph"]["status"]); self.assertTrue(a[1]["data"]["graph"]["validation_refs"])
    def test_governance_blocks_illegal_promotion(self):
        path=self.repo/".coder/demo-20260715/records/completion-input.json"; data=json.loads(path.read_text()); data["risks"][0]["state"]="ACCEPTED"; path.write_text(json.dumps(data))
        result,body=self.run_cli("--dry-run"); self.assertNotEqual(0,result.returncode); self.assertEqual("RISK_ACCEPTANCE_MISSING",body["issues"][0]["code"])
    def test_write_generates_card_index_and_strict_3w_summary(self):
        result,body=self.run_cli(); self.assertEqual(0,result.returncode,body)
        summary=(self.repo/".coder/demo-20260715/requirement-delivery-summary.md").read_text(); self.assertIn("## Why",summary); self.assertIn("## Who",summary); self.assertIn("## What",summary); self.assertNotIn("## How",summary)
        self.assertTrue((self.repo/".coder/_index/metadata.json").is_file())
if __name__=="__main__": unittest.main()
