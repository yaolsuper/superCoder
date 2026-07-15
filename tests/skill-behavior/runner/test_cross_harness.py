from __future__ import annotations
import json, unittest
from pathlib import Path
from adapter_runner import run
from compare_results import compare
ROOT=Path(__file__).resolve().parents[3]; REPO=ROOT/"tests/skill-behavior/fixtures/knowledge-cli/valid-repo"; ADAPTERS=["app-agent","opencode"]
class CrossHarnessTests(unittest.TestCase):
    def args(self,command,*extra): return [command,*extra,"--repo",str(REPO)]
    def test_same_json_exit_and_progressive_scope(self):
        for command,extra in (("metadata",("--project-id","demo-20260715")),("section",("--project-id","demo-20260715","--section","risks")),("entity",("--project-id","demo-20260715","--entity-id","evidence-1"))):
            result=compare(ADAPTERS,self.args(command,*extra)); self.assertTrue(result["semantic_equal"],result)
        output=run("app-agent",self.args("section","--project-id","demo-20260715","--section","risks")).stdout
        self.assertIn("Risk risk-1",output); self.assertNotIn("Expected and actual changes",output); self.assertNotIn("test-report-1",output)
    def test_module_to_requirement_sections_then_evidence(self):
        # Rebuild is intentionally executed on a disposable fixture copy by index tests;
        # P27 uses exact project location plus the same semantic chain without mutating source.
        for adapter in ADAPTERS:
            for section in ("changes","risks","relationships"):
                proc=run(adapter,self.args("section","--project-id","demo-20260715","--section",section)); self.assertEqual(0,proc.returncode); self.assertEqual("PASS",json.loads(proc.stdout)["status"])
            evidence=run(adapter,self.args("entity","--project-id","demo-20260715","--entity-id","evidence-1")); self.assertEqual(0,evidence.returncode)
    def test_unknown_adapter_is_not_a_pass(self):
        with self.assertRaises(ValueError): run("static-walkthrough",self.args("metadata","--project-id","demo-20260715"))
if __name__=="__main__": unittest.main()
