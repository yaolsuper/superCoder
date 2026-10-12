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
    def test_failed_or_missing_validation_cannot_materialize_completion(self):
        path=self.repo/".coder/demo-20260715/records/completion-input.json"
        original=json.loads(path.read_text())
        card=self.repo/".coder/demo-20260715/requirement-knowledge-card.md"
        before=card.read_bytes()
        for validations in ([], [{**original['validations'][0], 'result':'FAILED'}]):
            with self.subTest(validations=validations):
                data=copy.deepcopy(original); data['validations']=validations
                path.write_text(json.dumps(data))
                for flags in ((), ('--dry-run',)):
                    result,body=self.run_cli(*flags)
                    self.assertNotEqual(0,result.returncode,body)
                    self.assertEqual('COMPLETION_EVIDENCE_FAIL',body['issues'][0]['code'])
                self.assertEqual(before,card.read_bytes())
                self.assertFalse((card.parent/'requirement-delivery-summary.md').exists())
                self.assertFalse((self.repo/'.coder/_index').exists())
    def test_pass_label_without_complete_validation_binding_is_rejected(self):
        path=self.repo/".coder/demo-20260715/records/completion-input.json"
        original=json.loads(path.read_text())
        for key,value in (('command',''),('target_refs',[]),('source_digest',''),('stale',True)):
            with self.subTest(key=key):
                data=copy.deepcopy(original); data['validations'][0][key]=value
                path.write_text(json.dumps(data))
                result,body=self.run_cli()
                self.assertNotEqual(0,result.returncode,body)
                self.assertEqual('COMPLETION_EVIDENCE_FAIL',body['issues'][0]['code'])
    def test_unvalidated_actual_change_or_false_reconciliation_is_rejected(self):
        path=self.repo/".coder/demo-20260715/records/completion-input.json"
        original=json.loads(path.read_text())
        variants=[]
        data=copy.deepcopy(original)
        data['actual_changes'].append({'ref':'sc://demo-repo/demo-20260715/change/uncovered','status':'ACTUAL'})
        variants.append(data)
        data=copy.deepcopy(original)
        data['expected_changes']=[{'ref':'expected-1','actual_refs':['missing-actual'],'evidence_refs':['fake-evidence']}]
        variants.append(data)
        for data in variants:
            with self.subTest(data=data):
                path.write_text(json.dumps(data))
                result,body=self.run_cli()
                self.assertNotEqual(0,result.returncode,body)
                self.assertEqual('COMPLETION_EVIDENCE_FAIL',body['issues'][0]['code'])
    def test_rejected_recompletion_preserves_previous_card_summary_and_index(self):
        self.assertEqual(0,self.run_cli()[0].returncode)
        files=[self.repo/'.coder/demo-20260715/requirement-knowledge-card.md',
               self.repo/'.coder/demo-20260715/requirement-delivery-summary.md',
               *sorted((self.repo/'.coder/_index').glob('*'))]
        before={p:p.read_bytes() for p in files}
        path=self.repo/'.coder/demo-20260715/records/completion-input.json'
        data=json.loads(path.read_text()); data['validations'][0]['result']='FAILED'
        path.write_text(json.dumps(data))
        self.assertNotEqual(0,self.run_cli()[0].returncode)
        self.assertEqual(before,{p:p.read_bytes() for p in files})
if __name__=="__main__": unittest.main()
