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


if __name__ == "__main__":
    unittest.main()
