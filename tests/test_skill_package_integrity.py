import tempfile
import shutil
import subprocess
import unittest
import zipfile
from pathlib import Path

import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_skill_package as checker


class SkillPackageIntegrityTest(unittest.TestCase):
    def write_skill(self, root: Path, description="Valid description.") -> Path:
        skill = root / "skills" / "demo"
        skill.mkdir(parents=True)
        path = skill / "SKILL.md"
        path.write_text(
            f"---\nname: demo\ndescription: {description}\n---\n\n# Demo\n\nBody.\n",
            encoding="utf-8",
        )
        return path

    def prepare_router(self, root: Path, route="`demo`") -> None:
        router = root / "skills" / "test-privateer"
        router.mkdir(parents=True, exist_ok=True)
        (router / "SKILL.md").write_text(
            f"---\nname: test-privateer\ndescription: Router\n---\n\n# Router\n\n## 路由地图\n\n| 当前需要 | 使用 |\n| --- | --- |\n| demo | {route} |\n",
            encoding="utf-8",
        )

    def prepare_docs(self, root: Path, count=1) -> None:
        (root / "README.md").write_text(f"Contains {count} 个 Skill.\n", encoding="utf-8")
        (root / "docs").mkdir()
        (root / "docs/guide.md").write_text(f"Contains {count} 个 Skill.\n", encoding="utf-8")

    def test_rejects_unquoted_colon_in_description(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = self.write_skill(root, "Use it: now")
            with self.assertRaisesRegex(checker.IntegrityError, rf"{re_escape(path)}:3:"):
                checker.validate_skill(path)

    def test_rejects_router_reference_to_missing_skill(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_skill(root)
            self.prepare_router(root, "`missing-skill`")
            self.prepare_docs(root, 2)
            with self.assertRaisesRegex(checker.IntegrityError, "missing-skill"):
                checker.validate_sources(root / "skills", (root / "README.md", root / "docs/guide.md"))

    def test_rejects_workbuddy_nested_path_and_missing_root_entry(self):
        with tempfile.TemporaryDirectory() as directory:
            package = Path(directory) / "package.zip"
            with zipfile.ZipFile(package, "w") as archive:
                archive.writestr("references/skills/foo/SKILL.md", "body")
            with self.assertRaisesRegex(checker.IntegrityError, "SKILL.md"):
                checker.validate_zip(package, checker.PackageProfile())

            nested = Path(directory) / "nested.zip"
            with zipfile.ZipFile(nested, "w") as archive:
                archive.writestr("SKILL.md", "body")
                archive.writestr("references/skills/foo.md", "body")
            with self.assertRaisesRegex(checker.IntegrityError, "references/skills/foo.md"):
                checker.validate_zip(nested, checker.PackageProfile())

    def test_accepts_flat_zip_and_reports_boundaries(self):
        with tempfile.TemporaryDirectory() as directory:
            package = Path(directory) / "package.zip"
            with zipfile.ZipFile(package, "w") as archive:
                archive.writestr("SKILL.md", "body")
                archive.writestr("references/foo.md", "body")
            checker.validate_zip(package, checker.PackageProfile())

    def test_real_router_is_checked_and_empty_extraction_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            skills = Path(directory) / "skills"
            shutil.copytree(ROOT / "skills", skills)
            router = skills / "test-privateer/SKILL.md"
            original = router.read_text()
            checker.validate_sources(skills, ())
            self.assertIn("shaping-ai-tasks", checker.routed_names(router))
            for altered, error in (
                (original.replace("`shaping-ai-tasks`", "`missing-audit-skill`"), "missing-audit-skill"),
                (original.replace("## 路由地图", "## moved routes"), "路由"),
                (original[:original.index("## 路由地图")] + "## 路由地图\n\n## 词汇\n", "路由"),
            ):
                with self.subTest(error=error):
                    router.write_text(altered)
                    with self.assertRaisesRegex(checker.IntegrityError, error):
                        checker.validate_sources(skills, ())
                    result = subprocess.run(
                        [sys.executable, str(ROOT / "scripts/check_skill_package.py"), "--root", directory],
                        capture_output=True, text=True,
                    )
                    self.assertEqual(result.returncode, 1)
                    self.assertIn(str(router), result.stderr)
                    self.assertIn(error, result.stderr)


def re_escape(value: Path) -> str:
    return str(value).replace("\\", "\\\\").replace(".", "\\.")


if __name__ == "__main__":
    unittest.main()
