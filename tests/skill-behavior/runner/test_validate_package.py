from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
VALIDATOR_PATH = REPOSITORY_ROOT / "skills/superCoder/scripts/validate_package.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_package", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load validator: {VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class PackageValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()

    def fixture_root(self) -> Path:
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        root = Path(temporary_directory.name)
        write(
            root / "skills/superCoder/SKILL.md",
            "---\nname: superCoder\ndescription: test skill\n---\n\n# Test\n",
        )
        write(
            root / "skills/superCoder/config/module-map.yaml",
            "modules:\n"
            "  - id: skill_pack\n"
            "    files:\n"
            "      - \"skills/superCoder/SKILL.md\"\n"
            "      - \"tests/skill-behavior/p1-example.md\"\n",
        )
        write(
            root / "tests/skill-behavior/scenarios.yaml",
            "version: 1\n"
            "scenarios:\n"
            "  - id: p1-example\n"
            "    markdown: p1-example.md\n"
            "    required_routes:\n"
            "      - skills/superCoder/SKILL.md\n"
            "    expected_verdicts:\n"
            "      - EXAMPLE_PASS\n"
            "    must_not:\n"
            "      - claim_false_pass\n",
        )
        write(root / "tests/skill-behavior/p1-example.md", "# P1 example\n")
        write(root / "README.md", "# Fixture\n")
        return root

    def issue_codes(self, root: Path) -> set[str]:
        result = self.validator.validate_repository(root)
        return {issue["code"] for issue in result["issues"]}

    def test_valid_minimal_package_passes(self) -> None:
        result = self.validator.validate_repository(self.fixture_root())
        self.assertEqual("PASS", result["status"], result["issues"])

    def test_wrong_case_module_path_is_detected(self) -> None:
        root = self.fixture_root()
        module_map = root / "skills/superCoder/config/module-map.yaml"
        module_map.write_text(
            module_map.read_text(encoding="utf-8").replace(
                "skills/superCoder/SKILL.md", "skills/supercoder/SKILL.md"
            ),
            encoding="utf-8",
        )
        self.assertIn("PATH_CASE_MISMATCH", self.issue_codes(root))

    def test_missing_module_path_is_detected(self) -> None:
        root = self.fixture_root()
        module_map = root / "skills/superCoder/config/module-map.yaml"
        module_map.write_text(
            module_map.read_text(encoding="utf-8")
            + '      - "skills/superCoder/references/missing.md"\n',
            encoding="utf-8",
        )
        self.assertIn("REFERENCE_MISSING", self.issue_codes(root))

    def test_invalid_skill_frontmatter_is_detected(self) -> None:
        root = self.fixture_root()
        write(root / "skills/superCoder/SKILL.md", "# Missing frontmatter\n")
        self.assertIn("FRONTMATTER_INVALID", self.issue_codes(root))

    def test_duplicate_scenario_id_is_detected(self) -> None:
        root = self.fixture_root()
        scenarios = root / "tests/skill-behavior/scenarios.yaml"
        scenarios.write_text(
            scenarios.read_text(encoding="utf-8")
            + "  - id: p1-example\n"
            + "    markdown: p1-example.md\n",
            encoding="utf-8",
        )
        self.assertIn("REGISTRY_DRIFT", self.issue_codes(root))

    def test_scenario_missing_from_module_map_is_detected(self) -> None:
        root = self.fixture_root()
        module_map = root / "skills/superCoder/config/module-map.yaml"
        module_map.write_text(
            module_map.read_text(encoding="utf-8").replace(
                '      - "tests/skill-behavior/p1-example.md"\n', ""
            ),
            encoding="utf-8",
        )
        self.assertIn("REGISTRY_DRIFT", self.issue_codes(root))

    def test_missing_human_confirmation_contract_is_detected(self) -> None:
        root = self.fixture_root()
        issues = self.validator.validate_human_confirmation_contract(root)
        self.assertTrue(issues)
        self.assertIn("REFERENCE_MISSING", {item["code"] for item in issues})

    def test_invalid_human_confirmation_contract_is_detected(self) -> None:
        root = self.fixture_root()
        for relative, tokens in self.validator.HUMAN_CONFIRMATION_CONTRACT.items():
            write(root / relative, "\n".join(tokens) + "\n")
        config = root / "skills/superCoder/config/human-confirmation-gate.yaml"
        config.write_text(
            config.read_text(encoding="utf-8").replace(
                "direct_transition_to_planning: false",
                "direct_transition_to_planning: true",
            ),
            encoding="utf-8",
        )
        issues = self.validator.validate_human_confirmation_contract(root)
        self.assertIn("HUMAN_CONFIRMATION_CONTRACT_INVALID", {item["code"] for item in issues})

    def test_repository_distribution_is_consistent(self) -> None:
        result = self.validator.validate_repository(REPOSITORY_ROOT)
        self.assertEqual("PASS", result["status"], result["issues"])


if __name__ == "__main__":
    unittest.main()
