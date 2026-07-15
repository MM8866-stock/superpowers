---
id: ultra-wait-timeout-not-blocked
title: Codex treats a wait timeout as no update yet
status: ready
tags: ultra-fork, codex, agent-lifecycle
quorum_tier: sentinel
quorum_max_time: 20m
---

This scenario supports the Codex Coding-Agent.

When Codex is ready, send this exact message:

"Read the Codex reference in the installed superpowers plugin, then create one
Agent whose whole job is to wait at least 8 seconds and write `delayed.txt`
containing exactly `DELAY_OK`. Collect it with `wait_agent`. Make the first wait
use a one-second timeout so it returns before completion, treat that as no
update yet, then wait again for the same Agent. Do not create a replacement
Agent and do not edit the file yourself."

Do not reinterpret the request or suggest a retry policy. Once Codex reports
`DELAY_OK`, stop. If it declares the first timeout a failure or creates a second
Agent, stop because the failure behavior has been observed.

## Acceptance Criteria

- Codex creates exactly one Agent and calls `wait_agent` at least twice.
- The first incomplete wait is treated as `no update yet`, not as blockage,
  failure, or a reason to create a replacement Agent.
- The same Agent completes during this run and writes `delayed.txt` containing
  exactly `DELAY_OK`.
- Codex does not invoke the unrelated bare `wait` tool.
