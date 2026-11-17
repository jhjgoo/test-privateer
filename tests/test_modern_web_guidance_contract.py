import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ModernWebGuidanceContractTest(unittest.TestCase):
    def test_reference_is_reachable_and_bounded(self):
        text = (ROOT / "skills/reviewing-ui-ux/references/modern-web-guidance.md").read_text()
        for phrase in (
            "legacy-scan",
            "候选",
            "不是产品缺陷本身",
            "真实渲染／操作证据",
            "记录工具版本",
        ):
            self.assertIn(phrase, text)
        self.assertIn("https://github.com/GoogleChrome/modern-web-guidance-src", text)

    def test_ui_and_automation_consumers_point_to_reference(self):
        consumers = {
            "reviewing-ui-ux": ROOT / "skills/reviewing-ui-ux/SKILL.md",
            "designing-test-automation": ROOT / "skills/designing-test-automation/SKILL.md",
            "router": ROOT / "skills/test-privateer/SKILL.md",
        }
        for name, path in consumers.items():
            with self.subTest(consumer=name):
                text = path.read_text()
                if name == "router":
                    self.assertIn("Modern Web Guidance", text)
                    self.assertIn("`reviewing-ui-ux`", text)
                else:
                    self.assertIn("modern-web-guidance.md", text)
                    self.assertIn("不能替代", text)


if __name__ == "__main__":
    unittest.main()
