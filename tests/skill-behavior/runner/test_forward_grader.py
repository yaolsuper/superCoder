from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from grade_forward_fixtures import grade
from prepare_forward_fixtures import prepare


class ForwardGraderTests(unittest.TestCase):
    def test_prepared_baseline_is_not_model_execution_evidence(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "forward"
            prepare(root)
            # PASS prose cannot make incomplete product behavior or missing ledgers pass.
            for case in ("staged", "goal", "light"):
                (root / (case + "-report.md")).write_text("PASS AUTO_ADVANCE_ALLOWED DONE\n")
            result = grade(root / "fixture-manifest.json")
            self.assertEqual("FAIL", result["overall"])
            records = {r["case_id"]: r for r in result["records"]}
            self.assertEqual("FAIL", records["goal"]["result"])
            self.assertFalse(records["goal"]["checks"]["actual_tests_pass"])
            self.assertEqual("FAIL", records["light"]["result"])
            self.assertFalse(records["light"]["checks"]["one_active_project"])

    def test_git_failure_cannot_prove_unchanged_product(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "forward"
            prepare(root)
            (root / "staged-report.md").write_text("Observed normal start wait.\n")
            (root / "staged/.git").rename(root / "staged/.git-hidden")
            result = grade(root / "fixture-manifest.json")
            staged = result["records"][0]
            self.assertEqual("FAIL", staged["result"])
            self.assertFalse(staged["checks"]["git_diff_available"])


if __name__ == "__main__":
    unittest.main()
