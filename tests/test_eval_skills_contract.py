import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise AssertionError(f"{path}: missing opening frontmatter delimiter")
    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise AssertionError(f"{path}: missing closing frontmatter delimiter") from error

    fields: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or ":" not in line:
            raise AssertionError(f"{path}: invalid frontmatter line: {line!r}")
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        if not re.fullmatch(r"[a-z][a-z0-9_-]*", key) or not value:
            raise AssertionError(f"{path}: invalid frontmatter field: {line!r}")
        if value[0] in "[{>|" or value.count("[") != value.count("]"):
            raise AssertionError(f"{path}: unsupported or incomplete YAML value: {line!r}")
        fields[key] = value
    return fields


class EvalSkillsContractTest(unittest.TestCase):
    def test_eval_skills_have_valid_entrypoints_and_references(self):
        expected = {
            "shaping-ai-tasks": [],
            "prompt-eval": ["references/prompt-review-patterns.md"],
            "agent-eval": [
                "references/agent-quality-model.md",
                "references/evaluator-checks.md",
            ],
        }
        for name, references in expected.items():
            skill_dir = ROOT / "skills" / name
            text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
            frontmatter = read_frontmatter(skill_dir / "SKILL.md")
            self.assertEqual(frontmatter.get("name"), name)
            self.assertTrue(frontmatter.get("description"))
            for reference in references:
                self.assertIn(reference, text)
                self.assertTrue((skill_dir / reference).is_file())

    def test_prompt_eval_owns_current_model_fit_and_does_not_require_skill_eval(self):
        text = (ROOT / "skills/prompt-eval/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("目标模型", text)
        self.assertIn("邻近正常场景", text)
        self.assertIn("证据不足", text)
        self.assertNotIn("调用 `skill-eval`", text)

    def test_agent_eval_is_quality_review_not_platform_builder(self):
        text = (ROOT / "skills/agent-eval/SKILL.md").read_text(encoding="utf-8")
        for term in (
            "设计测试",
            "审查现有评估",
            "比较版本",
            "分析失败",
            "environment_error",
            "invalid_case",
            "prompt-eval",
        ):
            self.assertIn(term, text)
        self.assertIn("不负责搭建评测平台", text)

    def test_main_router_and_docs_expose_both_skills(self):
        main = (ROOT / "skills/test-privateer/SKILL.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        general_guide = (ROOT / "docs/guide.md").read_text(encoding="utf-8")
        guide = (ROOT / "docs/developer-guide.md").read_text(encoding="utf-8")
        for name in ("shaping-ai-tasks", "prompt-eval", "agent-eval"):
            self.assertIn(f"`{name}`", main)
            self.assertIn(f"`{name}`", readme)
            self.assertIn(f"`{name}`", general_guide)
            self.assertIn(name, guide)
        skill_count = len(list((ROOT / "skills").glob("*/SKILL.md")))
        self.assertIn(f"{skill_count} 个 Skill", readme)
        self.assertIn(f"{skill_count} 个 Skill", general_guide)

    def test_shaping_ai_tasks_preserves_route_boundaries(self):
        text = (ROOT / "skills/shaping-ai-tasks/SKILL.md").read_text(encoding="utf-8")
        for term in (
            "高度",
            "深度",
            "范围",
            "验证",
            "clarifying-test-basis",
            "setting-test-mission",
            "外部验证",
            "任务契约",
        ):
            self.assertIn(term, text)
        self.assertIn("已经足够明确时直接放行", text)
        self.assertIn("不把推荐、方案草案或任务契约说成已经执行或验证", text)

    def test_shaping_ai_tasks_defines_checkable_exit_conditions(self):
        text = (ROOT / "skills/shaping-ai-tasks/SKILL.md").read_text(encoding="utf-8")
        for term in (
            "固定退出条件",
            "可观察对象与判定方式",
            "环境受阻",
            "静默放宽条件",
            "输出长度、活动量或阶段自述不是完成证据",
        ):
            self.assertIn(term, text)

    def test_agent_eval_owns_blind_run_and_trace_protocol(self):
        text = (ROOT / "skills/agent-eval/SKILL.md").read_text(encoding="utf-8")
        for term in (
            "防止评测意图泄漏",
            "不出现 `eval`、`test`、`judge`、`rubric`、`score`、`benchmark`、`candidate`",
            "匿名标签",
            "候选实际读取了哪些 Skill",
            "未确认加载",
            "不跨项目扫描私有会话记录",
            "目标失败场景和一个邻近正常场景",
            "方向性改善",
        ):
            self.assertIn(term, text)

        eval_root = ROOT / "evals/agent-eval"
        self.assertTrue((eval_root / "README.md").is_file())
        self.assertEqual(
            {path.name for path in (eval_root / "inputs").glob("*.md")},
            {"leaky-comparison.md", "self-report-only.md", "environment-noise.md", "trajectory-conflict.md"},
        )

    def test_shaping_ai_tasks_eval_covers_upgrade_and_passthrough_cases(self):
        eval_root = ROOT / "evals/shaping-ai-tasks"
        self.assertTrue((eval_root / "README.md").is_file())
        inputs = {path.name for path in (eval_root / "inputs").glob("*.md")}
        self.assertEqual(
            inputs,
            {
                "authorization.md",
                "environment-retrospective.md",
                "fact-vs-decision.md",
                "cross-disciplinary.md",
                "explicit-api.md",
                "oracle-gap.md",
                "raw-material.md",
                "vague-test.md",
            },
        )


class ExitAndHarnessContractTest(unittest.TestCase):
    def test_running_sessions_preserve_pause_and_resume(self):
        text = (ROOT / "skills/running-test-sessions/SKILL.md").read_text(encoding="utf-8")
        for term in (
            "暂停与恢复",
            "当前原子步骤边界",
            "冷启动恢复点",
            "继承已完成工作",
            "不重做已完成工作",
            "恢复点、测试资产或项目规则冲突时",
            "单会话简单任务无需恢复点",
            "恢复回复本身要交付可执行下一步",
        ):
            self.assertIn(term, text)

    def test_automation_generates_verified_project_driver(self):
        text = (ROOT / "skills/designing-test-automation/SKILL.md").read_text(encoding="utf-8")
        router = (ROOT / "skills/test-privateer/SKILL.md").read_text(encoding="utf-8")
        for term in (
            "生成项目产品验证器",
            "访谈仓库而不是用户",
            "不默认引入框架",
            "只读 doctor",
            "失败证据保留位置",
            "实际驱动一条已映射用户路径",
            "未实测的生成物只能标注为草案",
            "拒绝双实例驱动",
            "直达路径",
            "带未验证清单的草案",
            "接口服务也属于真实产品表面",
        ):
            self.assertIn(term, text)
        self.assertIn("需要生成可持续驱动真实产品的验证器／验证资产 | `designing-test-automation`", router)

        eval_root = ROOT / "evals/test-automation/verification-harness"
        self.assertTrue((eval_root / "README.md").is_file())
        self.assertEqual(
            {path.name for path in (eval_root / "inputs").glob("*.md")},
            {"existing-harness.md", "draft-only.md", "shared-session.md"},
        )


if __name__ == "__main__":
    unittest.main()
