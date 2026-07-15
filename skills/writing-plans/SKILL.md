---
name: writing-plans
description: Use when you have a spec or requirements for a multi-step task, before touching code
---

# Writing Plans

## Overview

Write implementation plans as logical change batches. Each task should deliver one coherent behavior or engineering outcome that can be reviewed, verified, and reverted independently.

Assume the implementer is skilled but starts with only the approved spec, repository instructions, and the plan. Provide exact boundaries and stable interfaces without duplicating the design or pre-writing the implementation.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Context:** If working in an isolated worktree, it should have been created via the `superpowers:using-git-worktrees` skill at execution time.

**Save plans to:** `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`
- (User preferences for plan location override this default)

## Scope Check

If the spec covers multiple independent subsystems, it should have been broken into sub-project specs during brainstorming. If it wasn't, suggest breaking this into separate plans — one per subsystem. Each plan should produce working, testable software on its own.

Do not create a large Goal or SDD workflow for a small task that fits one independently verifiable batch. For a large task with multiple batches, ask once at handoff whether to enable Goal + SDD; do not repeat that choice between tasks.

## Use The Approved Spec

- Reference the approved spec sections that govern each task.
- Do not copy or reproduce the spec or design in the plan.
- Restate only cross-cutting constraints that an isolated implementer could otherwise miss.
- Avoid large or complete code listings. Include code only when an interface, migration shape, or non-obvious algorithm would be ambiguous without it.

## File Structure

Before defining tasks, map out which files will be created or modified and what each one is responsible for. This is where decomposition decisions get locked in.

- Design units with clear boundaries and well-defined interfaces. Each file should have one clear responsibility.
- You reason best about code you can hold in context at once, and your edits are more reliable when files are focused. Prefer smaller, focused files over large ones that do too much.
- Files that change together should live together. Split by responsibility, not by technical layer.
- In existing codebases, follow established patterns. If the codebase uses large files, don't unilaterally restructure - but if a file you're modifying has grown unwieldy, including a split in the plan is reasonable.

This structure informs the task decomposition. Each task should produce self-contained changes that make sense independently.

## Task Right-Sizing

A task is one logical change batch with an independently verifiable outcome and one commit boundary. Fold setup, configuration, scaffolding, documentation, and their focused tests into the batch whose behavior needs them. Split only where a reviewer could accept one outcome while rejecting or reverting its neighbor.

Each task must define:

- the approved spec section and observable outcome;
- exact file scope and ownership boundaries;
- stable interfaces consumed or produced;
- acceptance behavior, including relevant failure behavior;
- the focused RED/GREEN or verification commands for the batch;
- one commit boundary.

Do not split a batch into mechanical read/edit/run micro-tasks. Do not combine independent subsystems into a batch that cannot be tested, reviewed, or reverted coherently.

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** Follow the approved spec and repository instructions. Use superpowers:subagent-driven-development for an approved large Goal, or superpowers:executing-plans for inline execution.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

**Approved Spec:** [`docs/superpowers/specs/YYYY-MM-DD-<feature>-design.md`](../specs/YYYY-MM-DD-<feature>-design.md)

## Global Constraints

[Only constraints that every isolated task must see — exact version floors, dependency limits, naming rules, or platform requirements. Reference the source section; do not reproduce design rationale.]

---
```

## Task Structure

````markdown
### Task N: [Component Name]

**Spec:** `[approved spec path]`, section `[section name]`

**Outcome:** [One observable, independently verifiable behavior or engineering result]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Interfaces:**
- Consumes: [existing contracts this batch relies on]
- Produces: [stable contracts later batches rely on]

**Acceptance behavior:**
- [observable success behavior]
- [relevant failure or rollback behavior]

**Implementation notes:**
- [Only non-obvious constraints, ordering, or algorithm details needed to avoid ambiguity]

**Focused verification:**
- RED: `[exact test command]` — expected failure: `[missing behavior]`
- GREEN: `[exact focused command]` — expected: PASS
- Batch check: `[exact targeted command]` — expected: PASS

**Commit:**

`git commit -m "feat: deliver component outcome"`
````

## No Placeholders

Each batch must contain enough concrete information to execute without guessing. These are **plan failures**:
- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "add validation" / "handle edge cases"
- "Write tests for the above" without naming behaviors and exact commands
- "Similar to Task N" without the concrete delta and interface
- Repeating the full approved spec or embedding a near-complete implementation
- References to types, functions, or methods not defined in any task

## Remember
- Exact file paths always
- Stable interfaces and observable behavior
- Exact focused commands with expected outcomes
- DRY, YAGNI, TDD, one coherent commit per logical batch

## Self-Review

After writing the complete plan, look at the spec with fresh eyes and check the plan against it. This is a checklist you run yourself — not a subagent dispatch.

**1. Spec coverage:** Skim each section/requirement in the spec. Can you point to a task that implements it? List any gaps.

**2. Placeholder scan:** Search your plan for red flags — any of the patterns from the "No Placeholders" section above. Fix them.

**3. Type consistency:** Do the types, method signatures, and property names you used in later tasks match what you defined in earlier tasks? A function called `clearLayers()` in Task 3 but `clearFullLayers()` in Task 7 is a bug.

**4. Over-fragmentation:** Are multiple tasks merely mechanical steps toward one behavior? Merge them into one logical batch.

**5. Oversized batches:** Does a task mix independent outcomes or require unrelated verification and rollback? Split it at the stable interface.

**6. Duplication:** Does the plan copy the approved spec or include large implementation listings? Replace them with section references, contracts, and focused notes.

If you find issues, fix them inline. No need to re-review — just fix and move on. If you find a spec requirement with no task, add the task.

## Execution Handoff

After saving the plan:

- For a normal multi-batch task, execute inline with `superpowers:executing-plans`.
- For a large engineering task that benefits from durable Goal state and multiple Agents, ask once whether to enable Goal + SDD.
- For a small one-batch task discovered during planning, do not manufacture a large Goal; execute the approved batch directly.

Use this handoff only for large work:

> "Plan complete and saved to `docs/superpowers/plans/<filename>.md`. This is a large multi-batch task. Enable Goal + SDD, or execute inline?"

Honor that answer for the whole plan unless the human partner changes it.
