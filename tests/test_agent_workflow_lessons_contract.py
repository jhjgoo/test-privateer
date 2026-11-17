import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class AgentWorkflowLessonsContractTest(unittest.TestCase):
    def test_blind_worker_contract_is_reused(self):
        worker = ROOT / "skills/running-test-loop/references/blind-test-worker.md"
        loop = ROOT / "skills/running-test-loop/SKILL.md"
        worker_text = worker.read_text(encoding="utf-8")
        loop_text = loop.read_text(encoding="utf-8")
        for phrase in ("BLOCKED", "隔离 handoff", "唯一合成者", "不得写成观察结果"):
            self.assertIn(phrase, worker_text)
        self.assertIn("references/blind-test-worker.md", loop_text)
        self.assertIn("第一行任务指令", loop_text)

    def test_lesson_candidates_have_durable_action_value(self):
        text = (ROOT / "skills/maintaining-project-lessons/SKILL.md").read_text(encoding="utf-8")
        for phrase in ("未来同类任务", "改变后续 Agent 或人的行动", "一次性偏好", "不晋升为规则"):
            self.assertIn(phrase, text)

    def test_solution_check_interrogates_repeated_special_cases(self):
        text = (ROOT / "skills/checking-solutions/SKILL.md").read_text(encoding="utf-8")
        for phrase in ("反复出现特判", "oracle 是否错位", "多个特殊分支"):
            self.assertIn(phrase, text)

    def test_test_design_removes_executor_nuance(self):
        design = (ROOT / "skills/designing-test-experiments/SKILL.md").read_text(encoding="utf-8")
        challenge = (ROOT / "skills/challenging-test-designs/SKILL.md").read_text(encoding="utf-8")
        for phrase in ("隐藏复杂度", "该测什么、怎么看、怎么判", "经验性说明"):
            self.assertIn(phrase, design)
        self.assertIn("凭经验解释目标、观察方式或判定规则", challenge)


if __name__ == "__main__":
    unittest.main()
