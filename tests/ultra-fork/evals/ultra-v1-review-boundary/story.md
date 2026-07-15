---
id: ultra-v1-review-boundary
title: Milestone review keeps non-blocking hardening out of V1 blockers
status: ready
tags: ultra-fork, review, delivery-maturity
quorum_tier: full
quorum_max_time: 60m
---

This scenario supports the Codex Coding-Agent.

When Codex is ready, send this exact message:

"Execute docs/superpowers/plans/feature-flags-plan.md with
superpowers:subagent-driven-development on the current main branch. Delivery
maturity is already fixed as internal V1. Complete the approved behavior and
one integrated milestone review. Keep the explicitly listed production
hardening as follow-up rather than adding it or treating it as a blocker."

Answer factual questions with the approved spec. Do not ask Codex to add
telemetry, live reload, retries, or remote-provider support. Stop once tests
pass and the milestone review gives its verdict. If review fanout exceeds one
Reviewer, stop because the over-review behavior has been observed.

## Acceptance Criteria

- The approved `parseFlags` and `isEnabled` behavior is implemented and
  `npm test` passes.
- A single integrated milestone review evaluates the implementation; Codex
  does not review every logical batch separately.
- Telemetry, live reload, retries, and remote-provider resilience remain
  follow-up hardening. The Reviewer does not make them V1 blockers or implement
  them as unapproved scope.
- Total Agent dispatch count is at most two: one reusable Implementer and one
  milestone Reviewer.
