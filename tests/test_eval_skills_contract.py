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
        for name in ("prompt-eval", "agent-eval"):
            self.assertIn(f"`{name}`", main)
            self.assertIn(f"`{name}`", readme)
            self.assertIn(f"`{name}`", general_guide)
            self.assertIn(name, guide)
        skill_count = len(list((ROOT / "skills").glob("*/SKILL.md")))
        self.assertIn(f"{skill_count} 个 Skill", readme)
        self.assertIn(f"{skill_count} 个 Skill", general_guide)


if __name__ == "__main__":
    unittest.main()
