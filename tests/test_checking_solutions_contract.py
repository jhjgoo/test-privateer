import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CheckingSolutionsContractTest(unittest.TestCase):
    def test_merged_skill_has_one_entrypoint_and_lazy_sdd_reference(self):
        skill_dir = ROOT / "skills/checking-solutions"
        text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        sdd = skill_dir / "references/sdd-contract-chain.md"
        framework = skill_dir / "references/framework-map.md"

        self.assertIn("name: checking-solutions", text)
        self.assertIn("references/sdd-contract-chain.md", text)
        self.assertTrue(sdd.is_file())
        self.assertTrue(framework.is_file())
        self.assertFalse((ROOT / "skills/challenging-change-specs").exists())
        for term in ("样例耦合", "作用点", "未验证"):
            self.assertIn(term, text)
        self.assertNotIn("ADDED/MODIFIED/REMOVED", text)
        self.assertIn("ADDED/MODIFIED/REMOVED", sdd.read_text(encoding="utf-8"))

    def test_router_and_current_docs_use_the_merged_name(self):
        paths = (
            ROOT / "skills/test-privateer/SKILL.md",
            ROOT / "README.md",
            ROOT / "docs/guide.md",
            ROOT / "docs/developer-guide.md",
        )
        for path in paths:
            text = path.read_text(encoding="utf-8")
            self.assertIn("checking-solutions", text, path)
            self.assertNotIn("challenging-change-specs", text, path)

    def test_sdd_branch_requires_sdd_artifacts_and_preserves_regression_checks(self):
        skill_dir = ROOT / "skills/checking-solutions"
        core = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        sdd = (skill_dir / "references/sdd-contract-chain.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("先依据框架或产物关系确认属于 SDD", core)
        self.assertNotIn("或用户要求实施前、实施后、归档前质检时", core)
        self.assertIn("测试先行或回归保护符合项目要求", sdd)


if __name__ == "__main__":
    unittest.main()
