import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest import mock
import zipfile


ROOT = Path(__file__).resolve().parents[1]


def load_script(relative):
    spec = importlib.util.spec_from_file_location(Path(relative).stem, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ProfileConflictTest(unittest.TestCase):
    def test_independent_writer_is_preserved_on_conflict_or_callback_failure(self):
        updater = load_script("skills/setup-test-privateer/scripts/update_profile.py")
        for initial in (False, True):
            for fail in (False, True):
                with self.subTest(initial=initial, fail=fail), tempfile.TemporaryDirectory() as d:
                    project = Path(d)
                    target = project / ".test-privateer/project.md"
                    if initial:
                        updater.update_profile(project, "original")
                    original = target.read_text() if initial else ""
                    ready, done = threading.Event(), threading.Event()

                    def writer():
                        if ready.wait(5):
                            target.write_text(original + "\n人工新备注\n")
                            done.set()

                    worker = threading.Thread(target=writer)
                    worker.start()

                    def prepare(candidate):
                        self.assertNotEqual(candidate, target)
                        ready.set()
                        self.assertTrue(done.wait(5))
                        if fail:
                            raise RuntimeError("formatter failed")

                    try:
                        with self.assertRaises(updater.ProfileReadbackError):
                            updater.update_profile(project, "changed", prepare_candidate=prepare)
                    finally:
                        ready.set()
                        worker.join(5)
                    self.assertEqual(target.read_text(), original + "\n人工新备注\n")
                    self.assertEqual(list(target.parent.iterdir()), [target])

    def test_post_publication_edit_is_not_rolled_back(self):
        updater = load_script("skills/setup-test-privateer/scripts/update_profile.py")
        with tempfile.TemporaryDirectory() as d:
            project = Path(d)
            target = updater.update_profile(project, "original")
            replace = updater.os.replace

            def replace_then_edit(*args, **kwargs):
                replace(*args, **kwargs)
                with target.open("a") as handle:
                    handle.write("\nnew human note\n")

            with mock.patch.object(updater.os, "replace", side_effect=replace_then_edit):
                with self.assertRaises(updater.ProfileReadbackError):
                    updater.update_profile(project, "new value")
            self.assertIn("new value", target.read_text())
            self.assertIn("new human note", target.read_text())


class XMindPreservationTest(unittest.TestCase):
    def setUp(self):
        self.converter = load_script("skills/exporting-test-cases-to-xmind/scripts/md_to_xmind.py")
        self.header = "| ID | 场景／前置条件 | 怎么操作 | 预期结果 | 额外来源 |\n| --- | --- | --- | --- | --- |\n"

    def test_zip_preserves_symbols_details_and_excluded_scope(self):
        markdown = ("# Cases\n## tc-P0\n### C-001 path\n- 准备账户\n1. 打开路径\n"
                    + self.header + r"| C-002 | C:\temp\file.txt | match \d+ then \n | a\|b | SPEC-2 |" + "\n"
                    + "## 附录历史\n" + self.header + "| C-OLD | old | old | old | old |\n"
                    + "### nested\n- 旧详情\n## tc-P1\n### C-003\n- 新详情\n")
        with tempfile.TemporaryDirectory() as d:
            source = Path(d) / "cases.md"
            source.write_text(markdown)
            output = self.converter.convert(source)
            with zipfile.ZipFile(output) as archive:
                root = json.loads(archive.read("content.json"))[0]["rootTopic"]
            text = json.dumps(root, ensure_ascii=False)
            def titles(node):
                return [node["title"]] + [t for c in node.get("children", {}).get("attached", []) for t in titles(c)]
            values = titles(root)
            for exact in (r"场景／前置：C:\temp\file.txt", r"操作：match \d+ then \n", "预期：a|b", "额外来源：SPEC-2", "- 准备账户", "1. 打开路径", "- 新详情"):
                self.assertIn(exact, values)
            self.assertNotIn("C-OLD", text)
            self.assertNotIn("旧详情", text)
            self.assertEqual([n["title"] for n in root["children"]["attached"]], ["tc-P0", "tc-P1"])
            self.assertEqual(source.read_text(), markdown)

    def test_invalid_rows_and_unsupported_details_do_not_produce_success(self):
        for body in (self.header + "| C-1 | missing |\n", "## tc-P0\n```json\n{}\n```\n", "## tc-P0\n  - nested detail\n"):
            with self.subTest(body=body), tempfile.TemporaryDirectory() as d:
                source = Path(d) / "cases.md"
                source.write_text(body)
                with self.assertRaisesRegex(ValueError, r"cases.md:\d+:"):
                    self.converter.convert(source)
                self.assertFalse(source.with_suffix(".xmind").exists())
                with self.assertRaises(ValueError):
                    self.converter.convert(source, source)
                self.assertEqual(source.read_text(), body)

    def test_installed_script_runs_from_unrelated_cwd(self):
        for location in ("repository/skills", ".agents/skills", "project/.agents/skills"):
            with self.subTest(location=location), tempfile.TemporaryDirectory() as d:
                root = Path(d)
                installed = root / location / "exporting-test-cases-to-xmind"
                shutil.copytree(ROOT / "skills/exporting-test-cases-to-xmind", installed)
                cwd = root / "unrelated"
                cwd.mkdir()
                source = cwd / "cases.md"
                source.write_text("# Cases\n" + self.header + "| C-1 | given | act | result | rule |\n")
                result = subprocess.run([sys.executable, str(installed / "scripts/md_to_xmind.py"), str(source)], cwd=cwd, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue(zipfile.is_zipfile(source.with_suffix(".xmind")))


if __name__ == "__main__":
    unittest.main()
