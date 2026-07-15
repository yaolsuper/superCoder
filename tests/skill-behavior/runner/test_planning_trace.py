from __future__ import annotations
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
class PlanningTraceTests(unittest.TestCase):
    def test_cp_sequence_and_mapping_are_explicit(self):
        planning=(ROOT/"skills/superCoder-planning/references/planning.md").read_text()
        checkpoint=(ROOT/"skills/superCoder-checkpoint/references/checkpoint.md").read_text()
        self.assertIn("Analysis → CP2-A → DISCOVERED provisional Card → CP2-K → Plan → CP3",planning)
        self.assertIn("expected_change_refs",planning); self.assertIn("PLAN_TRACE_GAP",checkpoint)
        self.assertIn("CP2-A 不得依赖尚不存在的 Card",planning)
if __name__=="__main__": unittest.main()
