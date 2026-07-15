---
id: ultra-final-scope-map
title: Goal completion maps approved requirements to commits and evidence
status: ready
tags: ultra-fork, completion, evidence
quorum_tier: full
quorum_max_time: 60m
---

This scenario supports the Codex Coding-Agent.

When Codex is ready, send this exact message:

"Execute docs/superpowers/plans/url-tools-plan.md end-to-end with
superpowers:subagent-driven-development on the current main branch. At Goal
completion, write the final requirement-to-evidence mapping to
docs/superpowers/evidence/final-scope-map.md. Map each approved requirement to
its commit and verification command; do not claim completion without fresh
evidence."

Answer plan questions briefly. Do not provide evidence values yourself. Stop
once Codex reports the Goal complete and the mapping file exists.

## Acceptance Criteria

- `slugify` and `makeUrl` implement approved requirements R1 and R2, and
  `npm test` passes.
- `docs/superpowers/evidence/final-scope-map.md` maps R1 and R2 separately to
  real hexadecimal commit SHAs and the verification command `npm test`.
- The final completion statement is supported by the mapping and fresh test
  evidence rather than a summary-only claim.
- The work and evidence file are committed in the launched checkout.
