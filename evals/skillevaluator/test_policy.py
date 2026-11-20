import tempfile
import unittest
from pathlib import Path

from skillevaluator.models.result import Severity
from skillevaluator.validators.policy import load_policy_file, load_profile
from skillevaluator.validators.schema import SchemaValidator


ROOT = Path(__file__).resolve().parents[2]
POLICY = load_policy_file(Path(__file__).with_name("policy.yaml"))
MANIFEST = "---\nname: sample\ndescription: 用于审查测试证据。\n---\n\n# 示例\n\n检查输入证据并报告缺口。\n"


class RepositoryPolicyTest(unittest.TestCase):
    def validate(self, manifest, policy=POLICY):
        with tempfile.TemporaryDirectory() as directory:
            skill_dir = Path(directory) / "sample"
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text(manifest, encoding="utf-8")
            return SchemaValidator(policy=policy).validate(skill_dir)

    def test_missing_author_is_visible_but_does_not_block(self):
        self.assertFalse(self.validate(MANIFEST, load_profile()).passed)
        result = self.validate(MANIFEST)
        self.assertTrue(result.passed)
        author = [finding for finding in result.findings if finding.check_name == "author_missing"]
        self.assertEqual(len(author), 1)
        self.assertEqual(author[0].severity, Severity.MEDIUM)

    def test_invalid_required_metadata_still_blocks(self):
        for manifest in (
            MANIFEST.replace("name: sample\n", ""),
            MANIFEST.replace("description: 用于审查测试证据。\n", ""),
            MANIFEST.replace("name: sample", "name: other"),
            MANIFEST.replace("name: sample", "name: Invalid_Name"),
            MANIFEST.replace("description: 用于审查测试证据。", "description: [broken"),
        ):
            with self.subTest(manifest=manifest):
                self.assertFalse(self.validate(manifest).passed)

    def test_malformed_supplied_author_still_blocks(self):
        manifest = MANIFEST.replace(
            "description:", "metadata:\n  author: invalid\ndescription:", 1
        )
        result = self.validate(manifest)
        self.assertFalse(result.passed)
        self.assertTrue(
            any(
                finding.check_name == "author_format" and finding.severity == Severity.HIGH
                for finding in result.findings
            )
        )

    def test_policy_keeps_other_default_severities(self):
        base = load_profile()
        for category, check, severity in (
            ("SCHEMA", "author_format", Severity.HIGH),
            ("WORKFLOWS", "author_format", Severity.HIGH),
            ("LICENSE", "invalid_license", Severity.HIGH),
            ("SECURITY", "unsafe_command", Severity.HIGH),
            ("SECRETS", "credential", Severity.CRITICAL),
        ):
            with self.subTest(category=category, check=check):
                self.assertEqual(
                    POLICY.severity_for(category, check, severity),
                    base.severity_for(category, check, severity),
                )

    def test_existing_package_schema(self):
        for manifest in sorted((ROOT / "skills").glob("*/SKILL.md")):
            with self.subTest(skill=manifest.parent.name):
                result = SchemaValidator(policy=POLICY).validate(manifest.parent)
                self.assertTrue(result.passed, result.findings)


if __name__ == "__main__":
    unittest.main()
