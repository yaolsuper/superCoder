from __future__ import annotations

import hashlib
import importlib.util
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
RUNNER_PATH = REPOSITORY_ROOT / "tests/skill-behavior/runner/run_scenarios.py"


def load_runner():
    spec = importlib.util.spec_from_file_location("run_scenarios", RUNNER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load runner: {RUNNER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RunnerContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.runner = load_runner()

    def scenario(self) -> dict[str, object]:
        return {
            "id": "p16-example",
            "expected_verdicts": ["DISCOVERY_PASS", "REGISTRY_PASS"],
            "must_not": ["claim_false_pass"],
        }

    def test_no_raw_execution_is_not_run(self) -> None:
        result = self.runner.score_scenario(self.scenario(), None)
        self.assertEqual("NOT_RUN", result["result"])

    def test_forbidden_outcome_fails(self) -> None:
        raw_output = "DISCOVERY_PASS REGISTRY_PASS claim_false_pass"
        result = self.runner.score_scenario(self.scenario(), raw_output)
        self.assertEqual("FAIL", result["result"])
        self.assertEqual(["claim_false_pass"], result["forbidden_outcomes_present"])

    def test_digest_is_calculated_from_unmodified_raw_output(self) -> None:
        raw_output = "DISCOVERY_PASS\nREGISTRY_PASS\n"
        result = self.runner.build_result_record(
            scenario=self.scenario(),
            raw_output=raw_output,
            model="deterministic-test",
            harness="unit-test",
            commit="abc123",
            started_at="2026-07-15T00:00:00Z",
            finished_at="2026-07-15T00:00:01Z",
        )
        expected = hashlib.sha256(raw_output.encode("utf-8")).hexdigest()
        self.assertEqual(expected, result["raw_output_digest"])
        self.assertEqual("PASS", result["result"])


if __name__ == "__main__":
    unittest.main()

