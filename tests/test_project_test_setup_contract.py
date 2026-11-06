import tempfile
import unittest
import importlib.util
import stat
import subprocess
import sys
from unittest import mock
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ProjectTestSetupContractTest(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def load_updater(self):
        path = ROOT / "skills/setup-test-privateer/scripts/update_profile.py"
        spec = importlib.util.spec_from_file_location("test_privateer_profile_updater", path)
        module = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(module)
        return module

    def load_fixture_builder(self):
        path = ROOT / "evals/project-test-setup/prepare_fixture.py"
        spec = importlib.util.spec_from_file_location(
            "project_test_setup_fixture_builder", path
        )
        module = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(module)
        return module

    def test_setup_skill_uses_one_optional_project_profile(self):
        text = self.read("skills/setup-test-privateer/SKILL.md")
        for term in (
            ".test-privateer/project.md",
            "调查、建议、确认、预览、写入、回读",
            "仓库事实",
            "用户确认",
            "推断",
            "未知",
            "临时运行状态",
            "每轮只确认一个",
            "不重复询问“是否保存”",
            "不调用 `checking-solutions`",
            "先读取 `AGENTS.md`",
            "事实和来源索引",
            "不得复制、引用或回显",
            "相对项目根目录",
            "after_write",
            "删除无效配置",
            "不在项目中留下第二份配置",
            "不运行产品测试",
            "不安装",
            "不配置模型",
            "不保存秘密值",
            "检查已选框架的当前就绪状态",
            "Python 包存在不等于官方 Skill 已安装",
            "询问用户是否安装",
            "只有用户明确确认后",
            "当前宿主的就绪结果只在本轮报告",
            "missing_official_skill",
            "awaiting_install_confirmation",
            "顶层就绪状态必须是",
            "不得同时把本轮顶层状态写成 `environment_error`",
            "安装位置和作用域由宿主安装能力与用户选择决定",
            "不得自行创建项目内 `skills/deepeval/`",
            "判断是否配置完整 Test Loop",
            "`inherited_from_source`",
            "`pending_user_confirmation`",
            "完整 Loop 就绪状态必须为 `blocked`",
            "不生成验证器、TCO、测试资产、CI 或测试代码",
        ):
            self.assertIn(term, text)

    def test_profile_template_has_managed_markers_and_source_pointers(self):
        text = self.read(
            "skills/setup-test-privateer/references/project-profile-template.md"
        )
        for term in (
            "<!-- test-privateer-managed:start -->",
            "<!-- test-privateer-managed:end -->",
            "适用范围",
            "权威来源",
            "测试入口与资产位置",
            "测试框架与驱动约定",
            "环境与安全边界",
            "身份、数据准备和清理",
            "质量门槛与责任角色",
            "证据位置、敏感性和保留策略",
            "缺陷平台与 Finding 升级边界",
            "验证器与健康检查入口",
            "盲测子代理隔离输出",
            "共享资源及串并行策略",
            "完整 Test Loop 就绪",
            "`awaiting_user_confirmation`",
            "已确认后续补建项",
            "未决配置",
        ):
            self.assertIn(term, text)
        self.assertIn("引用来源", text)
        self.assertIn("不复制", text)
        self.assertIn("不相对本文件使用 `../`", text)
        self.assertIn("不得读取、复制或回显秘密值", text)

    def test_router_exposes_setup_without_making_it_mandatory(self):
        router = self.read("skills/test-privateer/SKILL.md")
        routing = self.read("skills/test-privateer/references/artifact-routing.md")
        self.assertIn("初始化、配置或重新适配 Test Privateer", router)
        self.assertIn("`setup-test-privateer`", router)
        self.assertIn(".test-privateer/project.md", router)
        self.assertIn("不存在时继续", router)
        self.assertIn("## 项目测试配置", routing)
        self.assertIn("当前用户在其决策权限内", routing)
        self.assertIn("当前项目权威来源", routing)
        self.assertIn("项目配置中的已确认补充", routing)
        self.assertIn("宿主权限", routing)
        self.assertLess(router.index("AGENTS.md"), router.index(".test-privateer/project.md"))
        self.assertIn("项目强制安全规则", routing)

    def test_framework_specific_skills_require_an_explicit_project_choice(self):
        setup = self.read("skills/setup-test-privateer/SKILL.md")
        router = self.read("skills/test-privateer/SKILL.md")
        for text in (setup, router):
            self.assertIn("项目配置", text)
            self.assertIn("框架专项", text)
        self.assertIn("等待确认", setup)
        self.assertIn("用户明确指令", router)
        self.assertIn("不得因为已有专项 Skill 自动选择", setup)
        self.assertIn("自有框架", router)

    def test_profile_updater_creates_replaces_and_preserves_human_content(self):
        update_profile = self.load_updater().update_profile

        managed_v1 = "## 权威来源\n\n- `README.md`\n"
        managed_v2 = "## 权威来源\n\n- `.github/workflows/ci.yml`\n"
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            path = update_profile(project, managed_v1)
            first = path.read_text(encoding="utf-8")
            self.assertIn(managed_v1, first)

            path.write_text(
                "# 人工说明\n\n不要删除。\n\n" + first + "\n## 维护备注\n\n保留。\n",
                encoding="utf-8",
            )
            path.chmod(0o644)
            update_profile(project, managed_v2)
            second = path.read_text(encoding="utf-8")
            self.assertIn("不要删除。", second)
            self.assertIn("保留。", second)
            self.assertIn(managed_v2, second)
            self.assertNotIn(managed_v1, second)
            self.assertEqual(second.count("test-privateer-managed:start"), 1)
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o644)

            update_profile(project, managed_v2)
            self.assertEqual(path.read_text(encoding="utf-8"), second)

    def test_profile_updater_refuses_unmarked_files_and_readback_mismatch(self):
        updater = self.load_updater()
        ProfileReadbackError = updater.ProfileReadbackError
        UnmanagedProfileError = updater.UnmanagedProfileError
        update_profile = updater.update_profile

        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            path = project / ".test-privateer/project.md"
            path.parent.mkdir()
            path.write_text("# 人工配置\n", encoding="utf-8")
            with self.assertRaises(UnmanagedProfileError):
                update_profile(project, "## 权威来源\n")
            self.assertEqual(path.read_text(encoding="utf-8"), "# 人工配置\n")

        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)

            def corrupt(path: Path) -> None:
                path.write_text("corrupted", encoding="utf-8")

            with self.assertRaises(ProfileReadbackError):
                update_profile(project, "## 权威来源\n", after_write=corrupt)
            self.assertFalse((project / ".test-privateer/project.md").exists())

        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            path = update_profile(project, "## 权威来源\n\n- `README.md`\n")
            original = path.read_text(encoding="utf-8")

            def corrupt_existing(path: Path) -> None:
                path.write_text("corrupted", encoding="utf-8")

            with self.assertRaises(ProfileReadbackError):
                update_profile(
                    project,
                    "## 权威来源\n\n- `.github/workflows/ci.yml`\n",
                    after_write=corrupt_existing,
                )
            self.assertEqual(path.read_text(encoding="utf-8"), original)

    def test_profile_updater_preserves_crlf_and_rejects_missing_project(self):
        updater = self.load_updater()
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            path = project / ".test-privateer/project.md"
            path.parent.mkdir()
            original = (
                "# 配置\r\n\r\n人工说明\r\n"
                "<!-- test-privateer-managed:start -->\r\n"
                "## 权威来源\r\n\r\n- `old.yml`\r\n"
                "<!-- test-privateer-managed:end -->\r\n"
                "结尾说明\r\n"
            ).encode()
            path.write_bytes(original)
            path.chmod(0o644)
            updater.update_profile(project, "## 权威来源\n\n- `new.yml`\n")
            updated = path.read_bytes()
            self.assertTrue(updated.startswith(b"# \xe9\x85\x8d\xe7\xbd\xae\r\n\r\n"))
            self.assertTrue(updated.endswith("结尾说明\r\n".encode()))
            self.assertNotIn(b"\n", updated.replace(b"\r\n", b""))
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o644)

        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "misspelled-project"
            with self.assertRaises(NotADirectoryError):
                updater.update_profile(missing, "## 权威来源\n")
            self.assertFalse(missing.exists())

    def test_profile_updater_restores_after_callback_errors_and_permission_changes(self):
        updater = self.load_updater()
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            path = updater.update_profile(
                project, "## 权威来源\n\n- `README.md`\n"
            )
            path.chmod(0o600)
            original = path.read_text(encoding="utf-8")

            def corrupt_then_fail(path: Path) -> None:
                path.write_text("corrupted", encoding="utf-8")
                raise RuntimeError("sync failed")

            with self.assertRaises(updater.ProfileReadbackError):
                updater.update_profile(
                    project,
                    "## 权威来源\n\n- `.github/workflows/ci.yml`\n",
                    after_write=corrupt_then_fail,
                )
            self.assertEqual(path.read_text(encoding="utf-8"), original)
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)

            def recreate_with_broader_mode(path: Path) -> None:
                content = path.read_bytes()
                path.unlink()
                path.write_bytes(content)
                path.chmod(0o644)

            updater.update_profile(
                project,
                "## 权威来源\n\n- `README.md`\n",
                after_write=recreate_with_broader_mode,
            )
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)

        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)

            def delete_after_write(path: Path) -> None:
                path.unlink()

            with self.assertRaises(updater.ProfileReadbackError):
                updater.update_profile(
                    project,
                    "## 权威来源\n\n- `README.md`\n",
                    after_write=delete_after_write,
                )
            self.assertFalse((project / ".test-privateer/project.md").exists())

    def test_profile_updater_rejects_symlink_escape_and_cleans_failed_temp_file(self):
        updater = self.load_updater()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / "project"
            outside = root / "outside"
            project.mkdir()
            outside.mkdir()
            outside_profile = outside / "project.md"
            outside_profile.write_text("keep\n", encoding="utf-8")
            try:
                (project / ".test-privateer").symlink_to(
                    outside, target_is_directory=True
                )
            except OSError as error:
                self.skipTest(f"symbolic links are unavailable: {error}")
            with self.assertRaises(updater.UnmanagedProfileError):
                updater.update_profile(project, "## 权威来源\n")
            self.assertEqual(outside_profile.read_text(encoding="utf-8"), "keep\n")

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / "project"
            outside = root / "outside"
            project.mkdir()
            outside.mkdir()
            outside_profile = outside / "project.md"
            outside_profile.write_text("outside\n", encoding="utf-8")
            outside_profile.chmod(0o600)

            def replace_parent_with_symlink(path: Path) -> None:
                moved = project / ".test-privateer-before-link"
                path.parent.rename(moved)
                path.parent.symlink_to(outside, target_is_directory=True)

            with self.assertRaises(updater.ProfileReadbackError):
                updater.update_profile(
                    project,
                    "## 权威来源\n",
                    after_write=replace_parent_with_symlink,
                )
            self.assertEqual(
                outside_profile.read_text(encoding="utf-8"), "outside\n"
            )
            self.assertEqual(stat.S_IMODE(outside_profile.stat().st_mode), 0o600)

        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            with mock.patch.object(
                updater.os, "replace", side_effect=PermissionError("blocked")
            ):
                with self.assertRaises(updater.ProfileReadbackError):
                    updater.update_profile(project, "## 权威来源\n")
            profile_dir = project / ".test-privateer"
            self.assertEqual(list(profile_dir.iterdir()) if profile_dir.exists() else [], [])

        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            real_named_temporary_file = updater.tempfile.NamedTemporaryFile

            def failing_named_temporary_file(*args, **kwargs):
                delegate = real_named_temporary_file(*args, **kwargs)

                class PartialWrite:
                    @property
                    def name(self):
                        return delegate.name

                    def __enter__(self):
                        delegate.__enter__()
                        return self

                    def __exit__(self, *exc):
                        return delegate.__exit__(*exc)

                    def write(self, content):
                        delegate.write(content[:8])
                        delegate.flush()
                        raise OSError("disk full")

                return PartialWrite()

            with mock.patch.object(
                updater.tempfile,
                "NamedTemporaryFile",
                side_effect=failing_named_temporary_file,
            ):
                with self.assertRaises(updater.ProfileReadbackError):
                    updater.update_profile(project, "## 权威来源\n")
            profile_dir = project / ".test-privateer"
            self.assertEqual(list(profile_dir.iterdir()) if profile_dir.exists() else [], [])

    def test_profile_updater_cli_accepts_marker_body_only(self):
        script = ROOT / "skills/setup-test-privateer/scripts/update_profile.py"
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            managed = project / "managed.md"
            managed.write_text("## 权威来源\n\n- `README.md`\n", encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(script),
                    "--project",
                    str(project),
                    "--managed-content",
                    str(managed),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            profile = project / ".test-privateer/project.md"
            self.assertIn("## 权威来源", profile.read_text(encoding="utf-8"))

    def test_fixture_builder_refuses_existing_target_files_without_partial_write(self):
        builder = self.load_fixture_builder()
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            readme = target / "README.md"
            readme.write_text("keep me\n", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                builder.prepare_fixture("existing-rules", target)
            self.assertEqual(readme.read_text(encoding="utf-8"), "keep me\n")
            self.assertFalse((target / "AGENTS.md").exists())
            self.assertFalse((target / ".github/workflows/ci.yml").exists())

        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            (target / ".github").write_text("not a directory\n", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                builder.prepare_fixture("existing-rules", target)
            self.assertEqual(
                {path.name for path in target.iterdir()},
                {".github"},
            )

        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            outside = target.parent / f"{target.name}-outside-readme"
            try:
                (target / "README.md").symlink_to(outside)
            except OSError as error:
                self.skipTest(f"symbolic links are unavailable: {error}")
            try:
                with self.assertRaises(FileExistsError):
                    builder.prepare_fixture("existing-rules", target)
                self.assertFalse(outside.exists())
                self.assertFalse((target / "AGENTS.md").exists())
            finally:
                outside.unlink(missing_ok=True)

        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            original_open = Path.open

            def partially_failing_open(path, mode="r", *args, **kwargs):
                handle = original_open(path, mode, *args, **kwargs)
                if path.name != "README.md" or mode != "x":
                    return handle

                class PartialWrite:
                    def __enter__(self):
                        handle.__enter__()
                        return self

                    def __exit__(self, *exc):
                        return handle.__exit__(*exc)

                    def write(self, content):
                        handle.write(content[:8])
                        handle.flush()
                        raise OSError("disk full")

                return PartialWrite()

            with mock.patch.object(Path, "open", new=partially_failing_open):
                with self.assertRaises(OSError):
                    builder.prepare_fixture("existing-rules", target)
            self.assertEqual(list(target.iterdir()), [])

    def test_behavior_eval_covers_setup_boundaries(self):
        readme = self.read("evals/project-test-setup/README.md")
        for term in (
            "已有项目规则",
            "缺少环境决定",
            "无 TCO",
            "重复运行",
            "秘密信息",
            "回读差异",
            "项目已选框架",
            "自有 Agent 评测框架",
            "DeepEval 官方 Skill 缺失",
            "Skill 加载轨迹",
            "文件差异",
        ):
            self.assertIn(term, readme)
        self.assertEqual(
            {
                path.name
                for path in (ROOT / "evals/project-test-setup/inputs").glob("*.md")
            },
            {
                "existing-rules.md",
                "environment-choice.md",
                "no-tco.md",
                "rerun-profile.md",
                "secret-handling.md",
                "readback-mismatch.md",
                "selected-framework.md",
                "custom-agent-framework.md",
                "deepeval-readiness.md",
                "loop-governance-gap.md",
                "loop-verifier-unconfirmed.md",
                "loop-verifier-deferred.md",
                "ordinary-no-profile.md",
                "profile-conflict.md",
            },
        )
        builder = self.load_fixture_builder()
        self.assertEqual(set(builder.FIXTURES), {path.stem for path in (
            ROOT / "evals/project-test-setup/inputs"
        ).glob("*.md")})
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            builder.prepare_fixture("rerun-profile", target)
            profile = (target / ".test-privateer/project.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("退款检查由支付质量组维护", profile)
            self.assertIn(".github/workflows/test.yml", profile)
            self.assertTrue((target / ".github/workflows/quality.yml").is_file())
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            builder.prepare_fixture("no-tco", target)
            self.assertTrue((target / "tests/test_health.py").is_file())
            self.assertTrue((target / "scripts/check_api.py").is_file())
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            builder.prepare_fixture("selected-framework", target)
            for relative in (
                "tests/unit/example.test.ts",
                "scripts/api-check.mjs",
                "e2e/smoke.spec.ts",
            ):
                self.assertTrue((target / relative).is_file(), relative)
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            builder.prepare_fixture("profile-conflict", target)
            self.assertTrue((target / "AGENTS.md").is_file())
            self.assertTrue((target / ".test-privateer/project.md").is_file())
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            builder.prepare_fixture("loop-governance-gap", target)
            self.assertTrue((target / "e2e/smoke.spec.ts").is_file())
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            builder.prepare_fixture("loop-verifier-deferred", target)
            self.assertIn(
                "Defect Hub",
                (target / "AGENTS.md").read_text(encoding="utf-8"),
            )


if __name__ == "__main__":
    unittest.main()
