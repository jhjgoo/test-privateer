import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class HumanCheckpointVocabularyTest(unittest.TestCase):
    def test_running_session_defines_checkpoint_contract(self):
        text = (ROOT / "skills/running-test-sessions/SKILL.md").read_text(
            encoding="utf-8"
        )
        section = text[text.index("## 人工检查点") : text.index("## 写回测试记录")]
        for field in (
            "负责人",
            "系统／环境",
            "页面／操作入口",
            "前置状态",
            "操作",
            "成功观察",
            "失败时保留证据",
            "回填位置",
            "恢复下一动作",
        ):
            self.assertIn(field, section)
        self.assertIn("待确认／待执行／执行中／已完成／失败／取消", section)
        self.assertIn("负责人提供的原始观察", section)
        self.assertIn("不套模板", section)
        self.assertIn("不重复生成同号检查点", section)

    def test_router_resumes_human_checkpoints_before_dependent_conclusions(self):
        text = (ROOT / "skills/test-privateer/SKILL.md").read_text(encoding="utf-8")
        boundary = text[text.index("## 上下文与阶段边界") : text.index("## 捷径与反例")]
        self.assertIn("人工检查点", boundary)
        self.assertIn("结果未回填前不推进依赖该步骤的结论", boundary)
        self.assertIn("不重复创建同号检查点", boundary)
        self.assertIn("running-test-sessions", boundary)

    def test_artifact_routing_owns_lightweight_vocabulary_layer(self):
        text = (
            ROOT / "skills/test-privateer/references/artifact-routing.md"
        ).read_text(encoding="utf-8")
        terms = text[text.index("## 测试术语") : text.index("## 面向读者的测试表达")]
        for term in ("测试项", "测试点", "测试条件", "测试模型", "探索章程", "探查"):
            self.assertIn(term, terms)
        for abbreviation in ("TCO", "SFDIPOT", "MFQ", "PPDCS"):
            self.assertIn(abbreviation, terms)
        self.assertIn("不重复方法细节", terms)
        self.assertIn("模型可派生测试条件", terms)
        self.assertIn("同一编号细化为测试条件时不改号", terms)


if __name__ == "__main__":
    unittest.main()
