"""Prompt-contract checks; behavioral evidence lives in evals/test-surface-language."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def section(text: str, heading: str) -> str:
    start = text.index(heading)
    end = text.find("\n## ", start + len(heading))
    return text[start:] if end == -1 else text[start:end]


class TestSurfaceContractTest(unittest.TestCase):
    def test_router_separates_test_level_from_tdd_and_completes_mixed_requests(self):
        text = (ROOT / "skills/test-privateer/SKILL.md").read_text(encoding="utf-8")
        routing = section(text, "## 路由当前缺口")

        self.assertIn(
            "测试层级由要取得的证据和观察位置决定；TDD 是实现新行为的反馈节奏，不是测试层级。",
            routing,
        )
        self.assertIn(
            "混合请求按交付物拆分，分别路由功能／接口 Case、单元测试或其他证据；所有已要求交付物都有结果或诚实状态后，当前请求才完成。",
            routing,
        )

    def test_functional_cases_follow_the_selected_test_surface(self):
        text = (
            ROOT / "skills/designing-test-experiments/SKILL.md"
        ).read_text(encoding="utf-8")
        cases = section(text, "## 表格优先交付 Case")

        for term in (
            "测试表面是执行者在当前层级能直接准备、操作和观察的边界",
            "所选测试表面",
            "执行者可操作、可观察",
            "公开 API Case",
            "移入技术依据",
            "改派到能控制该状态的测试层级",
        ):
            self.assertIn(term, cases)

    def test_api_design_keeps_public_contract_not_private_implementation(self):
        text = (ROOT / "skills/designing-test-automation/SKILL.md").read_text(
            encoding="utf-8"
        )
        boundary = section(text, "## 接口与页面入口的能力边界")

        self.assertIn("公开接口契约中的状态码与请求／响应字段", boundary)
        self.assertIn(
            "内部字段和实现组件不作为接口步骤或 oracle；有明确控制或观察入口时放在数据准备或技术依据中",
            boundary,
        )

    def test_unit_tests_keep_technical_names_at_the_selected_seam(self):
        text = (ROOT / "skills/writing-unit-tests/SKILL.md").read_text(
            encoding="utf-8"
        )
        writing = section(text, "## 4. 写清测试")

        self.assertIn("单元层 TDD", text)
        self.assertIn(
            "保留所选 seam 上的真实符号、输入输出类型、异常、fixture、替身和运行命令",
            writing,
        )

    def test_delivery_review_detects_test_surface_leakage(self):
        text = (ROOT / "skills/challenging-test-designs/SKILL.md").read_text(
            encoding="utf-8"
        )
        review = section(text, "## 检查分析链")

        self.assertIn("所选测试表面", review)
        self.assertIn("内部实现名", review)
        for term in ("真实符号", "类型", "fixture", "替身", "运行命令", "RED 证据"):
            self.assertIn(term, review)


if __name__ == "__main__":
    unittest.main()
