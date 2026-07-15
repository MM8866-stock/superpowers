import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


class SkillContractTests(unittest.TestCase):
    def test_brainstorming_sets_delivery_maturity_once(self):
        skill = read_text("skills/brainstorming/SKILL.md")

        self.assertRegex(skill, re.compile(r"delivery maturity", re.IGNORECASE))
        self.assertRegex(
            skill,
            re.compile(r"(decide|determine|set).{0,80}once", re.IGNORECASE | re.DOTALL),
        )
        self.assertRegex(
            skill,
            re.compile(r"do not (reopen|revisit).{0,80}delivery maturity", re.IGNORECASE),
        )

    def test_brainstorming_defers_non_blocking_production_hardening(self):
        skill = read_text("skills/brainstorming/SKILL.md")

        for blocker in (
            "deterministic correctness",
            "data corruption",
            "direct security risk",
        ):
            self.assertIn(blocker, skill.lower())
        self.assertRegex(
            skill,
            re.compile(
                r"non-blocking production hardening.{0,160}(defer|later version|follow-up)",
                re.IGNORECASE | re.DOTALL,
            ),
        )
        self.assertNotIn(
            "every project goes through this process",
            skill.lower(),
        )

    def test_writing_plans_uses_logical_batches(self):
        skill = read_text("skills/writing-plans/SKILL.md")

        self.assertRegex(skill, re.compile(r"logical (change )?batch", re.IGNORECASE))
        self.assertRegex(
            skill,
            re.compile(r"independently (verifiable|testable)", re.IGNORECASE),
        )
        self.assertNotIn("2-5 minutes", skill)
        self.assertNotIn("each step is one action", skill.lower())
        self.assertNotIn("every step must contain the actual content", skill.lower())

    def test_writing_plans_references_approved_spec_without_copying_it(self):
        skill = read_text("skills/writing-plans/SKILL.md")

        self.assertRegex(
            skill,
            re.compile(r"reference.{0,100}approved spec", re.IGNORECASE | re.DOTALL),
        )
        self.assertRegex(
            skill,
            re.compile(
                r"(do not|without).{0,100}(copy|duplicate|reproduce).{0,80}(spec|design)",
                re.IGNORECASE | re.DOTALL,
            ),
        )
        self.assertRegex(
            skill,
            re.compile(r"avoid.{0,100}(large|complete).{0,80}code", re.IGNORECASE),
        )

    def test_plan_review_detects_fragmentation_and_oversized_batches(self):
        prompt = read_text("skills/writing-plans/plan-document-reviewer-prompt.md")

        self.assertIn("Over-fragmentation", prompt)
        self.assertIn("Oversized batches", prompt)
        self.assertRegex(
            prompt,
            re.compile(r"mechanical.{0,80}(step|task)", re.IGNORECASE),
        )
        self.assertRegex(
            prompt,
            re.compile(r"single.{0,80}(review|verify|test)", re.IGNORECASE),
        )

    def test_sdd_dispatch_requires_purpose_and_positive_net_benefit(self):
        skill = read_text("skills/subagent-driven-development/SKILL.md")

        self.assertRegex(skill, re.compile(r"explicit purpose", re.IGNORECASE))
        self.assertRegex(
            skill,
            re.compile(r"positive expected net (value|benefit)", re.IGNORECASE),
        )
        self.assertRegex(
            skill,
            re.compile(r"do not dispatch.{0,100}fill capacity", re.IGNORECASE),
        )
        self.assertRegex(
            skill,
            re.compile(r"direct execution.{0,120}goal \+ sdd", re.IGNORECASE | re.DOTALL),
        )

    def test_sdd_reuses_implementers_and_runtime_selects_models(self):
        skill = read_text("skills/subagent-driven-development/SKILL.md")
        implementer = read_text(
            "skills/subagent-driven-development/implementer-prompt.md"
        )

        for phrase in ("same Goal", "responsibility", "logical batch"):
            self.assertIn(phrase.lower(), skill.lower())
        self.assertRegex(
            skill,
            re.compile(r"runtime.{0,100}(model|reasoning)", re.IGNORECASE),
        )
        self.assertRegex(
            skill,
            re.compile(r"inherit.{0,100}parent", re.IGNORECASE),
        )
        self.assertRegex(
            skill,
            re.compile(r"never claim.{0,100}downgrade", re.IGNORECASE),
        )
        self.assertNotIn("[MODEL", implementer)

    def test_sdd_enforces_write_wait_and_milestone_review_boundaries(self):
        skill = read_text("skills/subagent-driven-development/SKILL.md")

        for phrase in (
            "single writer",
            "isolated worktrees",
            "stable contracts",
            "non-overlapping ownership",
            "no update yet",
            "at most one integrated review per milestone",
            "existing implementation context",
            "recheck only",
        ):
            self.assertIn(phrase.lower(), skill.lower())

        reviewer_path = ROOT / "skills/subagent-driven-development/milestone-reviewer-prompt.md"
        self.assertTrue(reviewer_path.exists(), "milestone reviewer prompt is required")
        reviewer = reviewer_path.read_text(encoding="utf-8")
        self.assertIn("follow-up hardening", reviewer.lower())
        self.assertIn("already fresh", reviewer.lower())
        self.assertNotIn("[MODEL", reviewer)

    def test_sdd_uses_layered_tests_and_root_cause_convergence(self):
        skill = read_text("skills/subagent-driven-development/SKILL.md")

        for phrase in (
            "focused red/green",
            "logical-batch verification",
            "milestone gate",
            "root-cause convergence",
            "requirement-to-evidence mapping",
        ):
            self.assertIn(phrase.lower(), skill.lower())
        self.assertRegex(
            skill,
            re.compile(r"no fixed.{0,80}(time|token)", re.IGNORECASE),
        )

    def test_goal_ledger_contains_only_seven_durable_fields(self):
        ledger_path = ROOT / "skills/subagent-driven-development/goal-ledger-template.md"
        self.assertTrue(ledger_path.exists(), "goal ledger template is required")
        ledger = ledger_path.read_text(encoding="utf-8")
        headings = re.findall(r"^## (.+)$", ledger, re.MULTILINE)

        self.assertEqual(
            headings,
            [
                "Goal",
                "Current Milestone",
                "Completed Commits And Verification",
                "Active Agents And Responsibilities",
                "Current Real Issue",
                "Single Next Action",
                "Follow-Up Items",
            ],
        )

    def test_sdd_removes_mandatory_upstream_per_task_semantics(self):
        skill_dir = ROOT / "skills/subagent-driven-development"
        markdown = "\n".join(
            path.read_text(encoding="utf-8") for path in skill_dir.glob("*.md")
        ).lower()
        markdown += "\n" + read_text("skills/requesting-code-review/SKILL.md").lower()

        for forbidden in (
            "fresh subagent per task",
            "review after each task",
            "always specify the model explicitly",
            "task-reviewer-prompt.md",
            "full suite once before committing",
        ):
            self.assertNotIn(forbidden, markdown)
        self.assertFalse(
            (skill_dir / "task-reviewer-prompt.md").exists(),
            "per-task reviewer prompt must be removed",
        )

    def test_parallel_dispatch_requires_independence_and_positive_net_benefit(self):
        skill = read_text("skills/dispatching-parallel-agents/SKILL.md")

        self.assertRegex(
            skill,
            re.compile(
                r"independent.{0,120}positive expected net (value|benefit)",
                re.IGNORECASE | re.DOTALL,
            ),
        )
        self.assertRegex(skill, re.compile(r"explicit purpose", re.IGNORECASE))
        self.assertRegex(
            skill,
            re.compile(r"do not dispatch.{0,100}fill capacity", re.IGNORECASE),
        )

    def test_codex_reference_preserves_ultra_lifecycle_semantics(self):
        reference = read_text("skills/using-superpowers/references/codex-tools.md")
        lower = reference.lower()

        for phrase in (
            "ultra-native scheduling",
            "project and skill constraints",
            "inherit the parent configuration",
            "no update yet",
            "same run",
            "natural lifecycle",
            "imperfect strategy compliance",
        ):
            self.assertIn(phrase, lower)
        self.assertRegex(
            reference,
            re.compile(r"wait_agent.{0,120}not.{0,40}fail", re.IGNORECASE | re.DOTALL),
        )
        self.assertNotIn(
            "always close implementer and reviewer subagents",
            lower,
        )
        self.assertNotRegex(
            reference,
            re.compile(r"elapsed time.{0,80}(means|proves|is).{0,30}fail", re.IGNORECASE),
        )


if __name__ == "__main__":
    unittest.main()
