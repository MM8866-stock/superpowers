---
id: ultra-sdd-context-reuse
title: SDD reuses one healthy Implementer across related logical batches
status: ready
tags: ultra-fork, subagent-driven-development, context-reuse
quorum_tier: full
quorum_max_time: 60m
---

This scenario supports the Codex Coding-Agent.

When Codex is ready, send this exact message:

"Execute the approved plan at docs/superpowers/plans/name-tools-plan.md with
superpowers:subagent-driven-development. Use the current main branch in this
fixture. The two implementation batches share one responsibility area; reuse a
healthy Implementer when useful and perform no more than one integrated review
at the milestone. Finish with tests and commits."

Answer short factual questions from the plan. Do not recommend a fresh Agent or
extra review. Stop once both functions exist, tests pass, and Codex reports the
milestone complete. If three Agents have been created, stop because the
per-batch rebuild behavior has been observed.

## Acceptance Criteria

- Codex invokes `superpowers:subagent-driven-development` and uses at least one
  Agent.
- One healthy implementation context handles both related batches, or Codex
  gives concrete evidence for a natural rebuild boundary. It does not create a
  fresh Implementer merely because the plan moved to Task 2.
- At most one independent Reviewer is created for the milestone; total Agent
  dispatch count is one or two.
- `normalizeName` and `formatGreeting` are implemented, committed in coherent
  batches, and `npm test` passes in the launched checkout.
