---
id: ultra-small-task-no-goal
title: Small approved change bypasses Goal and Agent fanout
status: ready
tags: ultra-fork, cost, direct-execution
quorum_tier: sentinel
quorum_max_time: 20m
---

This scenario supports the Codex Coding-Agent.

When Codex is ready, send this exact message:

"The compact design in docs/superpowers/specs/greeting-design.md is approved.
Implement it, verify the result, and commit the change. This is one
self-contained batch; use direct execution unless a real blocker makes an
Agent necessary. You may work on the current main branch in this fixture."

Do not suggest Goal mode, SDD, review fanout, or extra features. If Codex asks
whether to use a Goal or Agent, answer: "Use your judgment and keep the process
proportionate." Once it reports completion, stop. If it creates two Agents,
stop immediately because the over-trigger behavior has already been observed.

## Acceptance Criteria

- `src/greeting.txt` contains exactly `hello world` followed by a newline.
- Codex completes the one-batch change without creating a subagent or Goal
  ledger.
- The change is committed and Codex reports focused verification evidence.
