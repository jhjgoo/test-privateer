"""Keep local validation output out of Git without hiding reusable sources."""

from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]


class RepositoryWorkflowTest(unittest.TestCase):
    def test_ignore_policy_separates_outputs_from_sources(self):
        ignored = {
            ".local/validation/review.md",
            "docs/research/local-audit.md",
            "docs/superpowers/plans/old-plan.md",
            "evals/test-surface-language/runs/example/output.md",
            "evals/history-regression/crossfile/runs/example/events.jsonl",
            "evals/report-language/export-check.xmind",
            "evals/history-regression/DECISION.md",
            "evals/history-regression/SHA256SUMS",
        }
        retained = {
            "skills/test-privateer/SKILL.md",
            "skills/exporting-test-cases-to-xmind/scripts/md_to_xmind.py",
            "tests/test_repository_workflow.py",
            "docs/guide.md",
            "docs/research/2026-09-15-sdd-frameworks-and-spec-gate.md",
            "evals/report-language/run.py",
            "evals/report-language/input.md",
            "evals/ui-ux/fixtures/profile-form.png",
            "evals/ui-ux/fixtures/SHA256SUMS",
            "evals/ui-ux/fixtures/reports/source.json",
            "evals/history-regression/crossfile/fixture/evidence/run-v1.txt",
            "openspec/specs/testing-workflow/spec.md",
            "openspec/changes/example/tasks.md",
            "openspec/changes/archive/2026-09-28-example/specs/example/spec.md",
        }
        result = subprocess.run(
            ["git", "-c", "core.excludesFile=/dev/null", "check-ignore",
             "--no-index", "--stdin"],
            cwd=ROOT, input="\n".join(sorted(ignored | retained)) + "\n",
            text=True, capture_output=True,
        )
        self.assertIn(result.returncode, (0, 1), result.stderr)
        self.assertEqual(set(result.stdout.splitlines()), ignored)


if __name__ == "__main__":
    unittest.main()
