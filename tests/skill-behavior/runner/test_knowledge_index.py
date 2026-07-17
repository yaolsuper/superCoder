from __future__ import annotations
import hashlib, json, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]; CLI=ROOT/"skills/superCoder/scripts/coder_knowledge.py"; FIXTURE=ROOT/"tests/skill-behavior/fixtures/knowledge-cli/valid-repo"

class KnowledgeIndexTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.repo=Path(self.tmp.name)/"repo"; shutil.copytree(FIXTURE,self.repo)
    def tearDown(self): self.tmp.cleanup()
    def run_cli(self,*args):
        result=subprocess.run([sys.executable,"-B",str(CLI),*args,"--repo",str(self.repo)],capture_output=True,text=True)
        return result,json.loads(result.stdout)
    def digest_index(self):
        return hashlib.sha256(b"".join(p.read_bytes() for p in sorted((self.repo/".coder/_index").glob("*")))).hexdigest()
    def test_rebuild_is_deterministic_and_validate_detects_stale(self):
        self.assertEqual(0,self.run_cli("rebuild-index")[0].returncode); before=self.digest_index()
        self.assertEqual(0,self.run_cli("rebuild-index")[0].returncode); self.assertEqual(before,self.digest_index())
        card=self.repo/".coder/demo-20260715/requirement-knowledge-card.md"; card.write_text(card.read_text()+"\n",encoding="utf-8")
        result,body=self.run_cli("validate-index"); self.assertNotEqual(0,result.returncode); self.assertEqual("INDEX_STALE",body["issues"][0]["code"])
    def test_failed_rebuild_preserves_old_index(self):
        self.assertEqual(0,self.run_cli("rebuild-index")[0].returncode); before=self.digest_index()
        card=self.repo/".coder/demo-20260715/requirement-knowledge-card.md"; card.write_text("broken",encoding="utf-8")
        self.assertNotEqual(0,self.run_cli("rebuild-index")[0].returncode); self.assertEqual(before,self.digest_index())
    def test_queries_are_bounded(self):
        self.assertEqual(0,self.run_cli("rebuild-index")[0].returncode)
        _,found=self.run_cli("find","--module","module-1","--limit","1"); self.assertEqual(1,len(found["data"]["requirements"]))
        ref="sc://demo-repo/demo-20260715/module/module-1"
        _,related=self.run_cli("related","--ref",ref,"--limit","2"); self.assertLessEqual(len(related["data"]["relations"]),2)

if __name__=="__main__": unittest.main()
