---
name: subagent-driven-development
description: Use when executing a large approved implementation plan that benefits from durable Goal state or purposeful subagents in the current session
---

# Subagent-Driven Development

Execute a large approved plan through durable milestones, logical batches, and purposeful Agent assistance. Reuse valuable implementation context instead of rebuilding it for every batch.

**Core principle:** Direct execution when coordination has no net benefit; Goal + SDD when purposeful delegation, durable recovery, or isolated parallelism has positive expected net value.

**Announce at start:** "I'm using Subagent-Driven Development to execute this Goal."

**Continuous execution:** After the human partner enables Goal + SDD, continue through approved batches without asking whether to proceed after each one. Stop only for a real blocker that requires their decision, an approved-scope contradiction, cancellation, or completion.

## Choose Direct Execution Or Goal + SDD

Use direct execution for a small task or one logical batch that the current Agent can complete coherently. Do not create a Goal, ledger, or long-lived Agent merely because the tools are available.

Use Goal + SDD when at least one of these is true:

- the approved plan has multiple milestones or logical batches;
- work is likely to cross context compaction, sessions, or tools;
- an Explorer, Implementer, or Reviewer has a clear specialized purpose;
- isolated worktrees permit genuinely independent work;
- durable evidence and recovery state materially reduce execution risk.

This is a value decision, not a size quota. Do not dispatch an Agent to fill capacity.

## Dispatch Purpose Gate

Before every dispatch, state four things in the controller's task record:

1. the Agent's **explicit purpose**;
2. the expected result and why delegation has **positive expected net value**;
3. the files or read-only scope it owns;
4. whether an existing Agent can continue instead.

No clear purpose or no net benefit means execute directly. Agent count is an outcome of useful decomposition, never a target.

Typical purposes:

- **Explorer:** answer one bounded codebase or dependency question without writing;
- **Implementer:** own one responsibility area and a coherent logical batch;
- **Reviewer:** independently assess a frozen milestone against approved scope and evidence.

Roles describe purpose, not permanent identities. The runtime may use native Agent capabilities as long as these boundaries remain clear.

## Runtime Model And Reasoning Selection

The current runtime chooses each Agent's concrete model and reasoning level within the parent task's configured ceiling. The Skill provides purpose, risk, and context; it does not maintain a fixed provider/model matrix.

- Prefer keeping an Agent's assigned capability stable while its responsibility and context remain stable.
- Change capability only at a natural boundary or after evidence shows the current assignment cannot complete the work.
- If explicit child model selection is unavailable, inherit the parent configuration.
- Never claim a downgrade, upgrade, or reasoning-level change that the runtime cannot enforce or verify.
- User and platform ceilings always override any recommendation.

## Reuse Before Rebuild

Prefer continuing a healthy Implementer when all three match:

- the same Goal;
- the same responsibility area;
- the same logical batch or its immediate review-fix continuation.

Context is healthy when the Agent can identify the current contract, changed files, latest evidence, and next action without reconstructing the project. Resume it with the new delta and relevant artifact paths, not the whole session history.

Create a new Agent at a natural rebuild boundary:

- responsibility moves to a different subsystem;
- the batch needs a materially different capability;
- context is stale, contradictory, or cannot be recovered from Git and the ledger;
- an independent milestone review is required;
- isolated parallel work has a stable contract and non-overlapping ownership.

Do not automatically close valid work because an Agent deviated from a preferred role or dispatch pattern. Correct future instructions and continue unless the work is actually unsafe, conflicting, failed, cancelled, or no longer useful.

## Execution Flow

1. **Read facts once.** Read the approved design, implementation plan, repository instructions, current Git state, and any existing Goal ledger. Trust committed facts over reconstructed conversation memory.
2. **Validate the plan.** Surface only contradictions that prevent correct execution. Record non-blocking hardening as follow-up instead of reopening approved V1 scope.
3. **Define milestones.** Group logical batches into independently demonstrable outcomes. Identify commit ranges and focused verification for each.
4. **Choose execution per batch.** Apply the purpose gate. Continue a healthy Implementer when reuse conditions hold; otherwise execute directly or dispatch at a natural boundary.
5. **Implement and verify.** Use focused TDD, keep one writer, commit the coherent batch, and record concise evidence.
6. **Review at milestone boundaries.** Use at most one integrated review per milestone, not a review after every batch.
7. **Finish with evidence.** Produce the final requirement-to-evidence mapping, run the project-required final gates once, then use superpowers:finishing-a-development-branch.

## Write Ownership

In a shared workspace, keep a **single writer**. Explorer and Reviewer Agents are read-only while the Implementer or controller writes.

Multiple writers are allowed only when all three conditions hold:

1. isolated worktrees;
2. stable contracts between the workstreams;
3. non-overlapping ownership of files and generated artifacts.

If any condition is missing, serialize the work. Do not rely on Agents informally avoiding each other's files.

## Focused Tests And Commit Boundaries

Use layered evidence instead of repeatedly running the largest suite:

- **Focused RED/GREEN:** the current test function or file proves the behavior was missing and then implemented;
- **Logical-batch verification:** targeted tests, lint, or build steps covering the changed contract;
- **Milestone gate:** the narrowest integration check that demonstrates the milestone outcome;
- **Final gate:** repository-required full checks once at the completion boundary, unless repository instructions explicitly require another cadence.

Each logical batch ends in one coherent commit unless the repository explicitly requires a different boundary. Do not split setup, implementation, tests, and docs into unrelated micro-commits when they form one outcome.

## Waiting And Progress

- A single wait timeout means **no update yet**. It does not prove blockage, failure, or lack of progress.
- Judge progress by concrete artifacts, reports, commits, test evidence, or a stated blocker—not elapsed time or one quiet wait.
- Use the runtime's follow-up mechanism when an Agent must take another turn; do not assume a queued message is an immediate answer.
- Do not interrupt a long-running Agent that is producing valid progress merely because a time or Token estimate was exceeded.

## Implementer Status

Implementers report one of four statuses:

- **DONE:** the logical batch is committed and focused evidence is recorded;
- **DONE_WITH_CONCERNS:** the batch is complete, but a concrete correctness or maintainability concern remains;
- **NEEDS_CONTEXT:** a named missing fact prevents safe progress;
- **BLOCKED:** the current approach cannot produce a valid outcome.

For NEEDS_CONTEXT, provide only the missing fact and continue the same Agent when its context is still valuable. For BLOCKED, diagnose the cause before retrying: missing context, wrong decomposition, invalid environment, capability mismatch, or plan contradiction. Never repeat the same request unchanged.

## Root-Cause Convergence

Use **root-cause convergence** when repeated attempts produce no new outcome. There are no fixed time or Token fuses.

1. Preserve the latest failure evidence and exact command or action.
2. Identify what changed between attempts; if nothing changed, do not retry.
3. Reduce to the smallest reproducible contract or environment check.
4. Fix the root cause or restructure the logical batch.
5. Continue the existing implementation context when it still holds useful knowledge.
6. Ask the human partner only when requirements, approved design, credentials, or external state must change.

Time alone is not a root cause. A wait timeout alone is not an attempt.

## Milestone Review

Run at most one integrated review per milestone. The milestone Reviewer reads:

- the approved design and plan;
- the frozen milestone commit range or review package;
- the Goal ledger;
- existing focused and milestone verification evidence;
- known follow-up hardening items.

The Reviewer checks approved behavior, material code quality, data semantics, direct security risks, and whether the evidence supports the claims. It separates current blockers from follow-up hardening and does not invent unapproved features or expand delivery maturity.

Send blockers back to the **existing implementation context** whenever it remains healthy. After fixes, recheck only the reported findings and the tests covering those fixes; do not start a new open-ended review. The final whole-branch review occurs once at the Goal completion boundary and may serve as the final milestone review.

## Durable Goal Ledger

Only large Goal work uses a ledger. Copy [goal-ledger-template.md](goal-ledger-template.md) to the project's agreed scratch or durable location. Update it at milestone completion, pause, compaction, session/tool handoff, or Goal completion—not after every command or wait.

The ledger contains only:

- Goal;
- current milestone;
- completed commits and verification;
- active Agents and responsibilities;
- current real issue;
- single next action;
- follow-up items.

After compaction or handoff, recover from the ledger, Git log, approved design, and verification evidence. Do not re-dispatch completed work because conversation memory is incomplete.

## File Handoffs

Prefer file artifacts over large copied prompts:

- `scripts/task-brief PLAN_FILE N` extracts one logical batch for an Implementer;
- the Implementer report records commits, focused TDD/tests, files, self-review, and concerns;
- `scripts/review-package BASE HEAD` freezes a commit range for milestone review;
- the Goal ledger records only durable recovery state.

Pass only the batch delta, stable interfaces, relevant prior decisions, and artifact paths. Do not make every Agent reread the whole repository or accumulated session history.

## Prompt Templates

- [implementer-prompt.md](implementer-prompt.md) — start or continue an Implementer for a logical batch
- [milestone-reviewer-prompt.md](milestone-reviewer-prompt.md) — integrated milestone review
- [goal-ledger-template.md](goal-ledger-template.md) — seven-field durable recovery record

## Red Flags

Never:

- start implementation on main/master without explicit human approval;
- create Agents to fill available capacity;
- create a new Implementer when a healthy one owns the same Goal, responsibility, and batch;
- hard-code or claim a child model/effort change the runtime cannot enforce;
- allow concurrent shared-workspace writers;
- infer failure from elapsed time or one wait timeout;
- review every batch by default;
- rerun a fresh broad suite merely to reconfirm reported output;
- retry an unchanged failing approach;
- turn follow-up hardening into an active V1 blocker;
- lose the link between approved requirements, commits, and verification evidence.

## Integration

**Required workflow skills:**

- **superpowers:using-git-worktrees** — create or verify isolation before implementation
- **superpowers:writing-plans** — create logical-batch plans
- **superpowers:test-driven-development** — drive behavior changes with RED/GREEN evidence
- **superpowers:verification-before-completion** — verify completion claims
- **superpowers:finishing-a-development-branch** — complete the branch after final evidence

Use **superpowers:systematic-debugging** when failures or unexpected behavior appear. Use **superpowers:requesting-code-review** only at a milestone or final branch boundary, not as a per-batch ritual.
