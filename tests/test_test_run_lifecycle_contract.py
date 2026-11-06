import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TestRunLifecycleContractTest(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_run_template_is_an_index_not_a_duplicate_report(self):
        text = self.read("skills/test-privateer/references/test-run-template.md")
        for term in (
            "RUN-<YYYYMMDD>-<NNN>",
            "testing/runs/<run-id>/run.md",
            "测试对象",
            "目标版本或快照",
            "授权",
            "禁止动作",
            "预算",
            "退出条件",
            "当前阶段",
            "轮次状态",
            "资产指针",
            "阻塞",
            "下一动作",
        ):
            self.assertIn(term, text)
        self.assertIn("只保存状态和指针", text)
        self.assertIn("不复制", text)

    def test_artifact_routing_defines_when_a_run_record_exists(self):
        text = self.read("skills/test-privateer/references/artifact-routing.md")
        for term in (
            "## 测试轮次资产",
            "testing/runs/<run-id>/run.md",
            "跨多个阶段",
            "跨会话",
            "人工检查点",
            "多个 Agent",
            "明确要求审计",
            "单会话、单项测试且方向不变",
            "不强制创建轮次记录",
        ):
            self.assertIn(term, text)

    def test_run_state_verdict_and_confidence_are_separate(self):
        template = self.read("skills/test-privateer/references/test-run-template.md")
        routing = self.read("skills/test-privateer/references/artifact-routing.md")
        for term in (
            "准备中",
            "可执行",
            "执行中",
            "已暂停",
            "受阻",
            "已完成",
            "已取消",
        ):
            self.assertIn(term, template)
        for text in (template, routing):
            self.assertIn("轮次状态", text)
            self.assertIn("测试判定", text)
            self.assertIn("测试信心", text)
        self.assertIn("已完成不表示测试通过", template)

    def test_one_synthesizer_owns_shared_assets_and_closed_runs_stay_closed(self):
        routing = self.read("skills/test-privateer/references/artifact-routing.md")
        running = self.read("skills/running-test-sessions/SKILL.md")
        for term in (
            "一个合成者",
            "隔离证据",
            "不得并发改写",
        ):
            self.assertIn(term, routing)
        self.assertIn("已完成或已取消", running)
        self.assertIn("新的 Run ID", running)
        self.assertIn("不改回执行中", running)

    def test_execution_checkpoints_and_decisions_share_the_run_id(self):
        text = self.read("skills/running-test-sessions/SKILL.md")
        for section_marker in ("### HCP-001", "### Resume-001", "### D-001"):
            start = text.index(section_marker)
            end = text.find("\n```", start)
            self.assertIn("Run ID", text[start:end])
        self.assertIn("恢复原 Run ID", text)

    def test_regression_and_confidence_use_current_run_evidence(self):
        regression = self.read("skills/selecting-regression-tests/SKILL.md")
        confidence = self.read("skills/assessing-test-confidence/SKILL.md")
        for text in (regression, confidence):
            self.assertIn("Run ID", text)
            self.assertIn("目标版本", text)
            self.assertIn("当前有效", text)
            self.assertIn("需要复核", text)
            self.assertIn("已被替代", text)
        self.assertIn("旧报告", confidence)
        self.assertIn("不得冒充本轮", confidence)

    def test_short_tasks_identify_evidence_without_inventing_a_run_id(self):
        artifact_spec = self.read(
            "openspec/specs/test-artifact-quality/spec.md"
        )
        regression = self.read("skills/selecting-regression-tests/SKILL.md")
        confidence = self.read("skills/assessing-test-confidence/SKILL.md")
        self.assertIn("存在轮次资产时", artifact_spec)
        for text in (artifact_spec, regression, confidence):
            self.assertIn("无 Run ID（单项短任务）", text)

    def test_legacy_run_verdicts_move_back_to_execution_records(self):
        running = self.read("skills/running-test-sessions/SKILL.md")
        self.assertIn("轮次记录含单项测试判定时", running)
        self.assertIn("移回执行记录", running)

    def test_case_execution_batches_preserve_run_history(self):
        text = self.read(
            "skills/designing-test-experiments/references/test-cases-template.md"
        )
        for term in (
            "Run ID",
            "目标版本或快照",
            "执行批次",
            "保留每次运行",
            "不覆盖历史",
        ):
            self.assertIn(term, text)

    def test_evidence_has_identity_retention_and_applicability(self):
        routing = self.read("skills/test-privateer/references/artifact-routing.md")
        for term in (
            "证据指针",
            "关联测试或 Finding ID",
            "目标版本",
            "环境",
            "生成时间",
            "实际来源",
            "敏感性",
            "保留期限",
            "清理前",
            "当前有效",
            "需要复核",
            "已被替代",
        ):
            self.assertIn(term, routing)
        self.assertIn("秘密值", routing)
        self.assertIn("CI Artifact", routing)

    def test_behavior_eval_checks_state_separation_real_merge_and_stable_hashes(self):
        readme = self.read("evals/test-run-lifecycle/README.md")
        resume_input = self.read(
            "evals/test-run-lifecycle/inputs/resume-payment-check.md"
        )
        parallel_input = self.read("evals/test-run-lifecycle/inputs/parallel-checks.md")
        self.assertIn("最终 `run.md` 不保留单项测试判定", readme)
        self.assertIn("旧格式", resume_input)
        self.assertIn("实际归并", parallel_input)
        self.assertIn("相对路径和文件内容", readme)
        for relative_path in (
            "evals/test-run-lifecycle/inputs/single-confidence.md",
            "evals/test-run-lifecycle/inputs/single-regression.md",
            "evals/test-run-lifecycle/fixtures/parallel-checks/"
            "evidence/RUN-20261105-004/C-101/result.json",
            "evals/test-run-lifecycle/fixtures/parallel-checks/"
            "evidence/RUN-20261105-004/C-102/result.json",
        ):
            self.assertTrue((ROOT / relative_path).is_file(), relative_path)


if __name__ == "__main__":
    unittest.main()
