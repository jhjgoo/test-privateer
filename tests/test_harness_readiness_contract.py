import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class HarnessReadinessContractTest(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_shared_reference_defines_six_stages_and_six_states(self):
        text = self.read(
            "skills/designing-test-automation/references/harness-readiness.md"
        )
        for stage in (
            "`Prepare`",
            "`Start`",
            "`Drive`",
            "`Observe`",
            "`Preserve`",
            "`Restore`",
        ):
            self.assertIn(stage, text)
        for state in (
            "`not_configured`",
            "`partial`",
            "`declared_unverified`",
            "`verified`",
            "`blocked`",
            "`not_applicable`",
        ):
            self.assertIn(state, text)
        self.assertIn("不是六个脚本", text)
        self.assertIn("不存在第七个 `stale` 状态", text)
        self.assertIn("不代表产品通过", text)
        self.assertIn("发现测试文件、脚本、依赖或命令不等于项目已经选择它", text)

    def test_setup_persists_harness_v2_without_running_products(self):
        skill = self.read("skills/setup-test-privateer/SKILL.md")
        template = self.read(
            "skills/setup-test-privateer/references/project-profile-template.md"
        )
        for term in (
            "test-privateer-project-profile/v2",
            "Harness 六段入口或缺口",
            "旧 v1",
            "不得自动迁移为 Harness `verified`",
            "框架名称",
            "不能单独产生 `verified`",
            "不把候选先写入长期配置再等待确认",
            "不能包含因框架、入口或适用性仍待决定而产生的 `not_configured`",
        ):
            self.assertIn(term, skill)
        for term in (
            "test-privateer-project-profile/v2",
            "六段入口／缺口",
            "Harness 状态",
            "Prepare／Start／Drive／Observe／Preserve／Restore",
        ):
            self.assertIn(term, template)
        self.assertIn("不运行产品测试", skill)
        self.assertIn("不安装", skill)

    def test_automation_owns_minimal_harness_construction(self):
        text = self.read("skills/designing-test-automation/SKILL.md")
        for term in (
            "建立或修复轻量 Harness",
            "轻量六段式 Harness",
            "`verified`",
            "`draft`",
            "`blocked`",
            "同一项目 Runner 可以覆盖多段",
            "不为统一形式新增服务、目录、注册中心或平行框架",
            "不得为获得 `verified` 修改被测产品代码",
        ):
            self.assertIn(term, text)

    def test_loop_checks_only_selected_surfaces_and_reuses_first_run(self):
        loop = self.read("skills/running-test-loop/SKILL.md")
        run_template = self.read(
            "skills/test-privateer/references/test-run-template.md"
        )
        for term in (
            "分析阶段侦察门禁与 Harness 检查",
            "进入详细风险模型、完整测试分析或用例扩展前",
            "对选中表面执行侦察门禁",
            "不要求全项目所有",
            "首个合适用例同时验证",
            "不为获得状态标签重复运行",
            "产品断言失败可以证明 Harness 有探错价值",
        ):
            self.assertIn(term, loop)
        for term in (
            "先建立最小 Run 合同和盲测任务包",
            "做一次有界侦察探针",
            "不先扩写 TCO、完整测试分析、详细用例集或回归计划",
            "受阻交付只需更新当前 Run 状态、探针证据、未执行范围、恢复入口和有界信心报告",
            "长期 Harness 标为 `verified`",
            "只做静态侦察并将运行时能力保留为未验证",
            "不再为满足盲测门槛重复同一覆盖指纹",
            "不再加载 Finding 调查、回归选择或与当前受阻结论无关的方法包",
        ):
            self.assertIn(term, loop)
        for term in (
            "本轮测试面与 Harness",
            "Harness 来源与状态快照",
            "本轮覆盖段",
            "实际执行／证据指针",
            "Restore／残留",
            "未覆盖或受阻",
        ):
            self.assertIn(term, run_template)

    def test_router_and_change_analysis_handoff_to_existing_skills(self):
        router = self.read("skills/test-privateer/SKILL.md")
        analysis = self.read("skills/analyzing-change-for-testing/SKILL.md")
        routing = self.read("skills/test-privateer/references/artifact-routing.md")
        self.assertIn(
            "测试表面的 Harness 能力需要判断、建立或补齐 | `designing-test-automation`",
            router,
        )
        self.assertIn("受影响的测试表面和需要的证据类型", analysis)
        self.assertIn("不在变化分析中运行或验证 Harness", analysis)
        self.assertIn("测试表面的六段 Harness 状态", routing)

    def test_behavior_eval_assets_cover_harness_boundaries(self):
        eval_root = ROOT / "evals/test-harness"
        self.assertEqual(
            {path.name for path in (eval_root / "inputs").glob("*.md")},
            {
                "setup-api-gap.md",
                "api-analysis-probe.md",
                "v1-migration.md",
                "unconfirmed-candidate.md",
                "ui-no-render.md",
                "agent-self-report.md",
                "single-stage-bypass.md",
            },
        )
        readme = (eval_root / "README.md").read_text(encoding="utf-8")
        for term in (
            "完整输出",
            "Skill 加载轨迹",
            "工具轨迹",
            "文件差异",
            "失败边界",
            "旧配置迁移",
            "未确认候选",
            "UI 无真实渲染",
            "分析阶段接口侦察",
            "Agent 只有自述",
            "单层请求旁路",
            "有界可执行性探针",
            "最小受阻交付",
        ):
            self.assertIn(term, readme)


if __name__ == "__main__":
    unittest.main()
