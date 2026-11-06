import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TestLoopContractTest(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_loop_skill_is_a_thin_orchestrator(self):
        text = self.read("skills/running-test-loop/SKILL.md")
        for term in (
            "启动契约",
            "Run ID",
            "授权",
            "禁止动作",
            "预算",
            "退出条件",
            "阶段状态",
            "当前缺口",
            "预期产生或更新的权威产物",
            "完成证据",
            "都不是推进证据",
            "即时加载",
            "不得为了预演完整流程一次性读取所有候选",
            "已复用或跳过的阶段不加载其专项",
            "handoff",
            "单一合成者",
            "最小充分",
            "不复制",
            "回边",
            "最近责任阶段",
            "只重验受影响路径",
            "不用旧聊天",
            "人工检查点",
            "暂停",
            "受阻",
            "不修改被测产品代码",
            "assessing-test-confidence",
        ):
            self.assertIn(term, text)
        for name in (
            "writing-api-tests",
            "writing-e2e-tests",
            "reviewing-ui-ux",
            "agent-eval",
            "investigating-findings",
            "selecting-regression-tests",
        ):
            self.assertIn(f"`{name}`", text)

    def test_router_separates_loop_from_single_stage_requests(self):
        router = self.read("skills/test-privateer/SKILL.md")
        self.assertIn("完整测试链", router)
        self.assertIn("`running-test-loop`", router)
        self.assertIn("单层", router)
        self.assertIn("不强制进入完整流程", router)
        self.assertIn("用户明确要求执行", router)

    def test_change_analysis_does_not_execute_without_authorization(self):
        text = self.read("skills/analyzing-change-for-testing/SKILL.md")
        for term in (
            "没有执行授权",
            "不得运行测试",
            "启动服务",
            "创建数据",
            "建议执行范围",
            "Test Loop",
            "已记录相应授权",
        ):
            self.assertIn(term, text)

    def test_loop_preserves_project_setup_and_run_contracts(self):
        loop = self.read("skills/running-test-loop/SKILL.md")
        router = self.read("skills/test-privateer/SKILL.md")
        self.assertIn(".test-privateer/project.md", loop)
        self.assertIn("testing/runs/<run-id>/run.md", loop)
        self.assertIn("项目配置不是授权", loop)
        self.assertIn("新的 Run ID", loop)
        self.assertIn("已完成或已取消", loop)
        self.assertIn("`running-test-loop`", router)

    def test_behavior_eval_assets_cover_loop_boundaries(self):
        eval_root = ROOT / "evals/test-loop"
        self.assertTrue((eval_root / "README.md").is_file())
        expected = {
            "api-only.md",
            "ui-rendered-evidence.md",
            "custom-agent-framework.md",
            "selected-framework-missing.md",
            "reuse-existing-cases.md",
            "human-checkpoint.md",
            "tool-failure.md",
            "retry-instability.md",
            "budget-stop.md",
            "pause-resume.md",
            "product-defect-readonly.md",
            "single-stage-bypass.md",
            "setup-readiness-gate.md",
            "resume-without-profile.md",
            "missing-stage-artifact.md",
            "targeted-rework.md",
            "development-context-blind.md",
            "duplicate-wave.md",
            "no-subagent-host.md",
            "high-risk-fanout.md",
            "operational-baseline.md",
        }
        self.assertEqual(
            {path.name for path in (eval_root / "inputs").glob("*.md")},
            expected,
        )
        readme = (eval_root / "README.md").read_text(encoding="utf-8")
        for term in (
            "Skill 加载轨迹",
            "工具轨迹",
            "文件差异",
            "失败边界",
            "API-only",
            "人工检查点",
            "暂停恢复",
            "产品代码只读",
            "Setup 就绪门禁",
            "阶段产物门禁",
            "最近责任阶段返工",
        ):
            self.assertIn(term, readme)

    def test_run_template_records_stage_gate_without_copying_artifacts(self):
        text = self.read("skills/test-privateer/references/test-run-template.md")
        for term in (
            "当前缺口",
            "输入指针",
            "预期权威产物",
            "阶段完成证据",
            "不构成阶段完成证据",
            "最近责任阶段",
            "不重启整条测试链",
        ):
            self.assertIn(term, text)

    def test_full_loop_requires_auditable_blind_subagents(self):
        text = self.read("skills/running-test-loop/SKILL.md")
        for term in (
            "冷启动盲测子代理",
            "盲测发现",
            "知情回归",
            "不得把开发聊天、实现理由",
            "不含结果的覆盖排除项",
            "同一子代理上下文",
            "新子代理会话不产生新的 Run ID",
            "封存 wave ID",
            "只写隔离 handoff",
            "`PASS`、`ISSUES` 或 `BLOCKED`",
            "没有实际执行证据",
            "覆盖指纹",
            "宿主不能创建",
            "项目 `AGENTS.md`／`CLAUDE.md`",
            "稳定操作基线",
            "全局 RTK",
            "全局／项目级 Skill",
            "获准 CLI",
            "不因全局安装、自动注入或父级继承而构成污染",
            "只有它包含开发聊天",
            "独立盲测未完成",
            "普通单层请求",
        ):
            self.assertIn(term, text)

    def test_full_loop_gates_on_project_readiness(self):
        text = self.read("skills/running-test-loop/SKILL.md")
        router = self.read("skills/test-privateer/SKILL.md")
        for term in (
            "项目就绪预检",
            "`not_configured`",
            "`awaiting_user_confirmation`",
            "`blocked`",
            "`ready`",
            "先进入 `setup-test-privateer`",
            "每轮向用户只提出一个",
            "不创建 Run",
            "不调度盲测子代理",
            "没有验证器时不得声称完整 Loop 可执行",
            "普通单层测试",
        ):
            self.assertIn(term, text)
        self.assertIn("完整测试链", router)
        self.assertIn("项目就绪预检", router)
        self.assertIn("旧 Run 缺少项目配置时", text)
        self.assertIn("不重复询问已确认的决定", text)
        prompt = self.read("evals/test-loop/inputs/setup-readiness-gate.md")
        self.assertNotIn("不要创建测试轮次", prompt)
        self.assertNotIn("不要执行产品测试", prompt)

    def test_run_template_indexes_blind_waves_without_copying_payloads(self):
        text = self.read("skills/test-privateer/references/test-run-template.md")
        for term in (
            "盲测 wave 索引",
            "子代理会话／任务 ID",
            "稳定操作基线／项目输入",
            "明确未披露的开发材料",
            "任务包哈希",
            "覆盖指纹",
            "隔离输出／证据指针",
            "不复制盲测 prompt、原始输出或证据正文",
            "全局 RTK",
            "全局／项目级 Skill",
            "获准 CLI",
            "不因自动注入、全局安装或父级继承而构成开发上下文污染",
            "新会话不创建新 Run ID",
        ):
            self.assertIn(term, text)

    def test_behavior_eval_assets_cover_blind_subagent_boundaries(self):
        eval_root = ROOT / "evals/test-loop"
        inputs = {path.name for path in (eval_root / "inputs").glob("*.md")}
        self.assertTrue(
            {
                "development-context-blind.md",
                "duplicate-wave.md",
                "no-subagent-host.md",
                "high-risk-fanout.md",
                "operational-baseline.md",
            }.issubset(inputs)
        )
        readme = (eval_root / "README.md").read_text(encoding="utf-8")
        for term in (
            "子代理调度",
            "候选输入",
            "上下文隔离",
            "覆盖指纹",
            "知情回归",
            "显式降级",
            "稳定操作基线",
        ):
            self.assertIn(term, readme)


if __name__ == "__main__":
    unittest.main()
