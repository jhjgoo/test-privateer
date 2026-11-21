import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "skills/running-test-loop/scripts/prepare_blind_brief.py"


class BlindBriefGeneratorTest(unittest.TestCase):
    def invoke(self, root, *extra):
        return subprocess.run(
            [
                sys.executable, str(SCRIPT),
                "--run-id", "RUN-1", "--wave-id", "payment",
                "--target-version", "v1", "--view", "付款重试",
                "--task", "同一付款意图只扣款一次",
                "--evidence-dir", "evidence/payment", "--synthesizer", "主会话",
                "--output", "delivery/payment.md", *extra,
                *([] if "--entry" in extra else [
                    "--command", sys.executable, "-c", "open('executed', 'w').close()",
                ]),
            ],
            cwd=root, capture_output=True, text=True,
        )

    def test_creates_resolvable_brief_without_executing_entry(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = self.invoke(root)
            self.assertEqual(result.returncode, 0, result.stderr)
            output = root / "delivery/payment.md"
            content = output.read_text()
            reference = content.splitlines()[0].split("`")[1]
            self.assertTrue((output.parent / reference).resolve().is_file())
            self.assertIn("同一付款意图只扣款一次", content)
            self.assertIn("evidence/payment", content)
            self.assertIn("唯一合成者：主会话", content)
            self.assertNotIn("不得写成观察结果", content)
            self.assertNotIn("不修改共享", content)
            self.assertFalse((root / "executed").exists())
            self.assertEqual(self.invoke(root).returncode, 0)
            self.assertEqual(output.read_text(), content)

    def test_preserves_conflicting_existing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "delivery").mkdir()
            output = root / "delivery/payment.md"
            output.write_text("existing evidence\n")
            self.assertNotEqual(self.invoke(root).returncode, 0)
            self.assertEqual(output.read_text(), "existing evidence\n")

    def test_preserves_non_command_entry_and_task_specific_prerequisites(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = self.invoke(
                root, "--entry", "隔离环境的付款确认页面",
                "--prerequisite", "使用已授权的普通用户测试账号",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            content = (root / "delivery/payment.md").read_text()
            for value in ("付款确认页面", "普通用户测试账号"):
                self.assertIn(value, content)

    def test_normalizes_output_before_creating_parent_directories(self):
        with tempfile.TemporaryDirectory() as directory:
            outer = Path(directory)
            root = outer / "work"
            root.mkdir()
            result = self.invoke(root, "--output", "../new-dir/../work/delivery/payment.md")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((root / "delivery/payment.md").is_file())
            self.assertFalse((outer / "new-dir").exists())

    def test_rejects_missing_contract_and_multiline_fields(self):
        for arguments in (
            ("--worker-contract", "missing.md"),
            ("--view", "付款\n额外共同规则"),
            ("--view", "付款\u2028额外共同规则"),
            ("--output", "../outside.md"),
        ):
            with self.subTest(arguments=arguments), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self.assertNotEqual(self.invoke(root, *arguments).returncode, 0)
                self.assertFalse((root / "delivery/payment.md").exists())


if __name__ == "__main__":
    unittest.main()
