from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills/superCoder/scripts/validate_trace_contract.py"
FIXTURES = ROOT / "tests/skill-behavior/fixtures/trace-contract"


def load_validator():
    spec = importlib.util.spec_from_file_location("trace_validator", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("trace validator is not loadable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TraceContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = load_validator()
        cls.valid = json.loads((FIXTURES / "valid/manifest.json").read_text())
        cls.cases = json.loads((FIXTURES / "invalid/cases.json").read_text())["cases"]

    def test_positive_fixture(self):
        result = self.validator.validate_manifest(self.valid)
        self.assertEqual("PASS", result["status"])
        self.assertEqual([], result["issues"])

    def test_negative_fixtures_have_stable_codes(self):
        for case in self.cases:
            with self.subTest(case=case["name"]):
                manifest = copy.deepcopy(self.valid)
                mutation = case["mutation"]
                if mutation == "duplicate_entity_id":
                    manifest["entities"].append(copy.deepcopy(manifest["entities"][0]))
                elif mutation == "unresolved_relation_target":
                    manifest["relations"][0]["target_ref"] += "-missing"
                elif mutation == "invalid_claim_state":
                    manifest["entities"][0]["status"] = "CLOSED"
                elif mutation == "remove_repository_id":
                    del manifest["repository_id"]
                elif mutation == "remove_evidence_relation":
                    manifest["relations"] = [r for r in manifest["relations"] if r["type"] != "ARGUMENT_SUPPORTED_BY_EVIDENCE"]
                elif mutation == "invalid_claim_owner":
                    manifest["entities"][0]["owner"] = "execution"
                elif mutation == "unknown_schema":
                    manifest["schema_version"] = "supercoder.trace/v999"
                codes = {issue["code"] for issue in self.validator.validate_manifest(manifest)["issues"]}
                self.assertIn(case["expected_code"], codes)


if __name__ == "__main__":
    unittest.main()
