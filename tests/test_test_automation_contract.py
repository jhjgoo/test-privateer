"""Text/link contracts only; agent and runtime evidence lives in evals/test-automation."""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/designing-test-automation"


class AutomationContractTest(unittest.TestCase):
    def test_implementation_route_and_e2e_reference_are_available(self):
        core = (SKILL / "SKILL.md").read_text()
        e2e = ROOT / "skills/writing-e2e-tests"
        self.assertIn("../writing-e2e-tests/SKILL.md", core)
        self.assertIn("只要求设计", core)
        self.assertIn("已有合适框架", core)
        self.assertTrue((e2e / "SKILL.md").is_file(), "Missing E2E implementation entry")
        if (e2e / "SKILL.md").is_file():
            self.assertIn("references/e2e-integration.md", (e2e / "SKILL.md").read_text())
        reference = e2e / "references/e2e-integration.md"
        self.assertTrue(reference.is_file(), "Missing scoped integration guide")
        if reference.is_file():
            text = reference.read_text()
            for term in ("版本", "本轮", "首次失败", "官方", "按需"):
                self.assertIn(term, text)

    def test_selected_method_references_are_reachable(self):
        core = (SKILL / "SKILL.md").read_text()
        links = re.findall(r"\]\((references/[^)#]+\.md)\)", core)
        for name in ("integration-contract-testing", "component-testing"):
            with self.subTest(reference=name):
                target = f"references/{name}.md"
                self.assertIn(target, links, "Missing method route")
                self.assertTrue((SKILL / target).is_file(), target)

    def test_methods_keep_sources_and_unit_routing(self):
        core = (SKILL / "SKILL.md").read_text()
        self.assertIn("writing-unit-tests", core)
        self.assertIn("按需", core)
        for path in (
            "writing-api-tests/SKILL.md",
            "writing-e2e-tests/SKILL.md",
            "designing-test-automation/references/integration-contract-testing.md",
            "designing-test-automation/references/component-testing.md",
        ):
            reference = ROOT / "skills" / path
            with self.subTest(reference=path):
                self.assertTrue(reference.exists(), "Missing sourced method")
                if reference.exists():
                    self.assertRegex(reference.read_text(), r"https://[^\s)]+")

    def test_direct_implementation_entries_are_discoverable_from_both_routers(self):
        for router in (SKILL / "SKILL.md", ROOT / "skills/test-privateer/SKILL.md"):
            for name in ("writing-api-tests", "writing-e2e-tests"):
                with self.subTest(router=router, entry=name):
                    target = ROOT / "skills" / name / "SKILL.md"
                    self.assertTrue(target.is_file(), "Missing directly usable entry")
                    self.assertIn(name, router.read_text())
                    if target.is_file():
                        self.assertIn(f"name: {name}", target.read_text())


if __name__ == "__main__":
    unittest.main()
