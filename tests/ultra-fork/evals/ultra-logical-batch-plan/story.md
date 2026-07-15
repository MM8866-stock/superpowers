---
id: ultra-logical-batch-plan
title: Approved design becomes a logical-batch plan without duplication
status: ready
tags: ultra-fork, writing-plans, cost
quorum_tier: sentinel
quorum_max_time: 30m
---

This scenario supports the Codex Coding-Agent.

When Codex is ready, send this exact message:

"The design at docs/superpowers/specs/contact-import-design.md is approved.
Write and commit the implementation plan only; do not implement it. Reference
the approved spec, organize the work as independently verifiable logical
batches, and avoid copying the design or writing complete implementation code."

If Codex asks whether the design is approved, answer "yes." If it asks about
execution mode, answer "planning only." Stop once a plan under
`docs/superpowers/plans/` is committed.

## Acceptance Criteria

- Codex writes an implementation plan under `docs/superpowers/plans/` and does
  not implement source code.
- The plan references `contact-import-design.md` and organizes the approved
  parser, store, and CLI outcomes into two to four logical batches.
- The plan names exact file scope, interfaces, focused verification, and one
  commit boundary per batch.
- The plan does not contain `2-5 minutes`, mechanical one-action steps, a copy
  of the design rationale, or near-complete implementation listings.
