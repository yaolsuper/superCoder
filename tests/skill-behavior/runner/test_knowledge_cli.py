from __future__ import annotations
import json, subprocess, sys, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CLI = ROOT / "skills/superCoder/scripts/coder_knowledge.py"
REPO = ROOT / "tests/skill-behavior/fixtures/knowledge-cli/valid-repo"

class KnowledgeCliTests(unittest.TestCase):
    def run_cli(self, *args: str):
        result = subprocess.run([sys.executable, "-B", str(CLI), *args, "--repo", str(REPO)], capture_output=True, text=True)
        return result, json.loads(result.stdout)

    def test_metadata_is_bounded(self):
        result, body = self.run_cli("metadata", "--project-id", "demo-20260715")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertNotIn("Expected and actual changes", result.stdout)
        self.assertEqual("Requirement", body["data"]["resource"]["type"])

    def test_section_returns_only_requested_content(self):
        result, body = self.run_cli("section", "--project-id", "demo-20260715", "--section", "changes")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("Expected and actual changes.\n", body["data"]["content"])
        self.assertNotIn("req-1", body["data"]["content"])

    def test_entity_returns_direct_relations_only(self):
        result, body = self.run_cli("entity", "--project-id", "demo-20260715", "--entity-id", "module-1")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("module-1", body["data"]["entity"]["id"])
        self.assertEqual(1, len(body["data"]["relations"]))

    def test_validate_card_and_module(self):
        self.assertEqual(0, self.run_cli("validate-card", "--project-id", "demo-20260715")[0].returncode)
        result, body = self.run_cli("validate-module", "--module-id", "module-1")
        self.assertEqual(0, result.returncode)
        self.assertEqual("CANDIDATE", body["data"]["resource"]["status"])

if __name__ == "__main__": unittest.main()
