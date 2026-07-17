from __future__ import annotations
import copy, importlib.util, json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]; MODULE=ROOT/"skills/superCoder/scripts/knowledge/lineage.py"; INPUT=ROOT/"tests/skill-behavior/fixtures/completion-materialization/valid-repo/.coder/demo-20260715/records/completion-input.json"
def load():
    spec=importlib.util.spec_from_file_location("lineage",MODULE); module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module
class LineageTests(unittest.TestCase):
    def setUp(self): self.module=load(); self.data=json.loads(INPUT.read_text())
    def test_valid_lineage(self): self.assertEqual([],self.module.validate_lineage(self.data["operations"],self.data["validations"]))
    def test_duplicate_and_parent_are_rejected(self):
        ops=copy.deepcopy(self.data["operations"]); ops.append(copy.deepcopy(ops[0])); ops[-1]["parent_event_id"]="missing"
        codes={x["code"] for x in self.module.validate_lineage(ops,self.data["validations"])}
        self.assertIn("EVENT_ID_DUPLICATE",codes); self.assertIn("PARENT_UNRESOLVED",codes)
    def test_not_run_validation_is_rejected(self):
        vals=copy.deepcopy(self.data["validations"]); vals[0]["result"]="NOT_RUN"
        self.assertIn("VALIDATION_NOT_EXECUTED",{x["code"] for x in self.module.validate_lineage(self.data["operations"],vals)})
if __name__=="__main__": unittest.main()
