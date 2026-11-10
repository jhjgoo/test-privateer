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
            "prepare_candidate",
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
            "安装位置和作用域由宿主安装能力与用户选择决定",
            "不得自行创建项目内 `skills/deepeval/`",
            "判断是否配置完整 Test Loop",
            "`inherited_from_source`",
            "`pending_user_confirmation`",
            "完整 Loop 就绪状态必须为 `blocked`",
            "通过 `mapping-project-test-space` 初始化或校准项目 TCO",
            "TCO 是普通项目初始化的核心产物",
            "partial: tco_not_initialized",
            "不能用空标题或模板占位冒充全景图",
            "不生成验证器、需求测试资产、CI 或测试代码",
            "test-privateer-project-profile/v2",
            "顶层 Setup 状态使用",
            "轻量六段式 Harness",
            "`not_configured`",
            "`partial`",
            "`declared_unverified`",
            "`verified`",
            "不得新增 `stale` 状态",
            "用一个权威资产索引统一记录",
            "不创建空目录或占位文件",
            "每个已调查的候选测试表面都保留一行",
            "Harness 状态只使用",
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
            "Setup 状态",
            "权威测试资产索引",
            "测试框架与驱动约定",
            "环境与安全边界",
            "身份、数据准备和清理",
            "质量门槛与责任角色",
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

    def test_profile_template_exposes_setup_surface_and_asset_state(self):
        text = self.read(
            "skills/setup-test-privateer/references/project-profile-template.md"
        )
        for term in (
            "配置契约版本",
            "test-privateer-project-profile/v2",
            "Setup 状态",
            "最近校准时间",
            "依据版本或来源快照",
            "失效条件",
            "当前阻塞",
            "恢复入口",
            "Harness 状态",
            "六段入口／缺口",
            "最近长期证据",
            "`not_configured`",
            "`partial`",
            "`declared_unverified`",
            "`verified`",
            "适用性未知时写待确认和取证动作",
            "`not_applicable` 需要项目来源或用户决定",
            "权威测试资产索引",
            "维护责任",
            "访问边界",
            "保留／失效条件",
            "盲测子代理隔离输出",
        ):
            self.assertIn(term, text)
        self.assertNotIn("## 证据位置、敏感性和保留策略", text)

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

    def test_ordinary_setup_confirms_test_surfaces_and_governance(self):
        setup = self.read("skills/setup-test-privateer/SKILL.md")
        template = self.read(
            "skills/setup-test-privateer/references/project-profile-template.md"
        )
        for term in (
            "不是 Loop 专属字段",
            "普通 Setup 也调查",
            "测试框架选择属于普通 Setup",
            "没有入口不等于不需要",
            "已有单元框架也不代表其他表面已配置",
            "等待确认",
            "不把未知默认为不适用",
        ):
            self.assertIn(term, setup)
        for term in (
            "该核对适用于普通 Setup",
            "缺少框架不代表不需要该类测试",
            "当前不开展须有明确决定",
            "CI 必需检查与门禁含义",
            "项目治理前置项",
            "Harness 状态",
            "权威测试资产索引",
        ):
            self.assertIn(term, template)

    def test_setup_bootstraps_tco_without_duplicating_mapping_method(self):
        setup = self.read("skills/setup-test-privateer/SKILL.md")
        mapping = self.read("skills/mapping-project-test-space/SKILL.md")
        template = self.read(
            "skills/setup-test-privateer/references/project-profile-template.md"
        )
        for term in (
            "读取 `mapping-project-test-space/SKILL.md`",
            "唯一 `testing/TCO.md`",
            "建立有依据的草案",
            "项目目标与使用者",
            "关键业务／系统链",
            "覆盖节点与已有保护",
            "长期风险／未知",
            "只要已有证据足以形成项目基线",
            "partial: tco_not_initialized",
            "不能宣称 Setup 完成",
            "不写入长期项目配置",
            "只能依据当前工具轨迹",
            "不得用配置草稿或模型自述",
        ):
            self.assertIn(term, setup)
        for method in ("SFDIPOT", "MFQ", "analyzing-product-risks"):
            self.assertIn(method, mapping)
        self.assertIn(
            "| 项目 TCO | `testing/TCO.md`", template
        )
        self.assertIn("缺失原因和恢复入口", template)

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
                update_profile(project, "## 权威来源\n", prepare_candidate=corrupt)
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
                    prepare_candidate=corrupt_existing,
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

    def test_profile_updater_preserves_target_after_candidate_errors_and_permissions(self):
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
                    prepare_candidate=corrupt_then_fail,
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
                prepare_candidate=recreate_with_broader_mode,
            )
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)

        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)

            def delete_prepare_candidate(path: Path) -> None:
                path.unlink()

            with self.assertRaises(updater.ProfileReadbackError):
                updater.update_profile(
                    project,
                    "## 权威来源\n\n- `README.md`\n",
                    prepare_candidate=delete_prepare_candidate,
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
                    prepare_candidate=replace_parent_with_symlink,
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

    def test_lifecycle_fixture_has_a_real_failing_signal(self):
        builder = self.load_fixture_builder()
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            builder.prepare_fixture("lifecycle-project", project)
            command = [sys.executable, "scripts/check_catalog.py"]
            original = subprocess.run(command, cwd=project, capture_output=True, timeout=10)
            self.assertEqual(original.returncode, 0, original.stderr)
            # The driver must detect a wrong business result, not merely exit successfully.
            (project / "src/catalog.py").write_text("def lookup(code):\n    return -1\n")
            broken = subprocess.run(command, cwd=project, capture_output=True, timeout=10)
            self.assertNotEqual(broken.returncode, 0)
            self.assertIn(b"AssertionError", broken.stderr)

    def test_stale_asset_fixture_exposes_real_evidence_and_a_missing_record(self):
        builder = self.load_fixture_builder()
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            builder.prepare_fixture("stale-assets", project)
            command = [sys.executable, "-B", "scripts/check_catalog.py", "-v"]
            result = subprocess.run(command, cwd=project, capture_output=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(b"Ran 2 tests", result.stderr)
            self.assertFalse((project / "openspec/changes/catalog-check/evidence/api.txt").exists())
            (project / "src/catalog.py").write_text("def lookup(code):\n    return 120\n")
            broken = subprocess.run(command, cwd=project, capture_output=True, timeout=10)
            self.assertNotEqual(broken.returncode, 0)
            self.assertIn(b"KeyError not raised", broken.stderr)

    def test_behavior_eval_covers_setup_boundaries(self):
        readme = self.read("evals/project-test-setup/README.md")
        for term in (
            "已有项目规则",
            "缺少环境决定",
            "默认初始化缺少 TCO",
            "用户明确排除 TCO",
            "重复运行",
            "秘密信息",
            "回读差异",
            "项目已选框架",
            "自有 Agent 评测框架",
            "DeepEval 官方 Skill 缺失",
            "普通配置的框架缺口",
            "普通配置的治理缺口",
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
                "tco-bootstrap.md",
                "rerun-profile.md",
                "secret-handling.md",
                "readback-mismatch.md",
                "selected-framework.md",
                "ordinary-framework-scope.md",
                "ordinary-governance-gap.md",
                "custom-agent-framework.md",
                "deepeval-readiness.md",
                "loop-governance-gap.md",
                "loop-verifier-unconfirmed.md",
                "loop-verifier-deferred.md",
                "ordinary-no-profile.md",
                "profile-conflict.md",
                "release-scope.md",
                "release-scope-confirmed.md",
                "lifecycle-setup.md",
                "lifecycle-develop.md",
                "lifecycle-archive.md",
                "lifecycle-unrelated.md",
                "lifecycle-no-rules.md",
                "mixed-install.md",
                "aligned-install.md",
                "stale-assets.md",
                "late-scope.md",
                "late-scope-confirmed.md",
            },
        )
        builder = self.load_fixture_builder()
        inputs = {path.stem for path in (
            ROOT / "evals/project-test-setup/inputs"
        ).glob("*.md")}
        shared_inputs = {
            "release-scope-confirmed", "lifecycle-setup", "lifecycle-develop",
            "lifecycle-archive", "lifecycle-unrelated", "lifecycle-no-rules",
        }
        self.assertEqual(set(builder.FIXTURES), (inputs - shared_inputs) | {"lifecycle-project"})
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
            builder.prepare_fixture("tco-bootstrap", target)
            self.assertTrue((target / "docs/architecture.md").is_file())
            self.assertTrue((target / "docs/api.md").is_file())
            self.assertFalse((target / "testing/TCO.md").exists())
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
            builder.prepare_fixture("ordinary-framework-scope", target)
            self.assertTrue((target / "tests/unit/order.test.ts").is_file())
            self.assertIn(
                "尚未决定接口检查",
                (target / "docs/api-contract.md").read_text(encoding="utf-8"),
            )
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            builder.prepare_fixture("ordinary-governance-gap", target)
            self.assertTrue((target / ".github/workflows/ci.yml").is_file())
            self.assertFalse((target / "testing/TCO.md").exists())
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
