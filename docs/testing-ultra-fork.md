# Testing The Ultra-First Fork

The fork uses three evaluation layers. A green lower layer does not replace a
higher layer; each answers a different question.

## Layer 1: Deterministic Contracts

Run after every Skill behavior change:

```bash
tests/ultra-fork/run-tests.sh
```

These tests reject known regressions such as per-task fresh Implementers,
per-task reviews, fixed model routing, repeated maturity questions, mechanical
plans, and wait-timeout failure inference.

## Layer 2: Normal Codex Scenarios

Install and statically validate the fork-owned Quorum overlay:

```bash
scripts/install-fork-evals.sh --check
```

The script reuses an existing ignored `evals/` checkout or clones
`prime-radiant-inc/superpowers-evals`, copies only the six `ultra-*` scenarios,
sets `SUPERPOWERS_ROOT` to this fork, and runs `quorum check`. Static checking
does not launch a Coding-Agent.

Run scenarios sequentially to keep attribution clear:

```bash
cd evals
export SUPERPOWERS_ROOT="$(git -C .. rev-parse --show-toplevel)"
for scenario in \
  ultra-small-task-no-goal \
  ultra-logical-batch-plan \
  ultra-sdd-context-reuse \
  ultra-wait-timeout-not-blocked \
  ultra-v1-review-boundary \
  ultra-final-scope-map
do
  bun run quorum run "scenarios/$scenario" --coding-agent codex
done
```

Live Codex runs require `~/.codex/auth.json` to contain ChatGPT subscription
authentication (`auth_mode: chatgpt`), not API-key authentication. Quorum's
Gauntlet-Agent also needs one supported QA credential, such as
`ANTHROPIC_API_KEY` or `CLAUDE_CODE_OAUTH_TOKEN`. Check only the presence and
auth mode when troubleshooting; never print or commit credential values.

Do not automatically retry `fail` or `indeterminate`. Inspect the first run and
attribute the result to the Skill, Codex runtime, fixture, credential, or Quorum
before deciding whether another run is valid.

## Layer 3: Real Ultra Acceptance

At a major SDD milestone, run two trusted local tasks with the user's current
GPT-5.6 Ultra configuration:

1. a two-to-three-batch backend change that should reuse one Implementer and
   review once at the milestone;
2. mixed exploration and implementation with one delayed Agent result and a
   non-blocking production-hardening suggestion.

Record only sanitized counts and outcomes: Agent count, reuse, review count,
test count, wall time, final result, strategy deviations, and unresolved fork
defects. Do not commit raw transcripts, credentials, personal paths, or project
content. Imperfect strategy compliance is acceptable when final quality and
safety boundaries hold.
