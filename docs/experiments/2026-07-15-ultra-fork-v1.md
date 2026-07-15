# Ultra-First Fork V1 Evaluation Record

Date: 2026-07-15

This record contains sanitized commands, verdicts, counts, and unresolved
release gates only. Raw transcripts and run directories remain ignored.

## Provenance

- Fork branch under test: `codex/ultra-fork`
- Fork baseline before eval overlay: `a27e952`
- Quorum checkout: `485d43a`
- Bun: `1.3.14`
- Codex CLI: `0.144.1`
- Coding-Agent target: `codex`

## Layer 1: Contracts

Command:

```bash
tests/ultra-fork/run-tests.sh
```

Verdict before adding the overlay: 13 tests passed. The final contract count is
recorded again at the evaluation-overlay commit boundary.

## Layer 2: Quorum Static Check

Command:

```bash
scripts/install-fork-evals.sh --check
```

Verdict: pass. Quorum accepted all six fork-owned scenarios and the credential
schema without launching a Coding-Agent.

Scenario count: 6.

## Layer 2: Normal Codex Live Run

First attempted command:

```bash
cd evals
bun run quorum run scenarios/ultra-small-task-no-goal --coding-agent codex
```

Verdict: `indeterminate` during setup.

Sanitized reason: the available Codex CLI login used API-key authentication;
the Quorum `codex` harness requires ChatGPT subscription authentication. The
auth file shape was inspected without printing credential values.

The other five scenarios were not launched because they share the same failed
precondition. This follows the no-blind-retry rule and avoids six identical paid
or indeterminate starts.

Observed counts:

- completed Coding-Agent sessions: 0
- Agent dispatches: unavailable
- reviews: unavailable
- test commands by Coding-Agent: unavailable
- wall time for the failed preflight: under 1 second

## Layer 3: Real Ultra Acceptance

Status: not run in this inline implementation session.

Required release evidence remains:

1. a new task using the user's selected GPT-5.6 Ultra mode for a two-to-three
   batch backend change, recording Implementer reuse and one milestone review;
2. a new Ultra task mixing exploration and implementation with one delayed
   Agent result and one non-blocking production-hardening suggestion.

These runs must occur after the fork is installed and selected. The current
session cannot prove that a new task used the user's UI-selected Ultra mode, so
it does not substitute an ordinary Codex CLI run or fabricated counts.

## Unresolved Gates And Defects

- Environment gate: replace or separately provision the Codex CLI API-key login
  with ChatGPT subscription auth before normal Codex Quorum runs.
- Environment gate: provide a supported Gauntlet-Agent credential before live
  Quorum execution.
- Release gate: run the six normal Codex scenarios once after auth is ready.
- Release gate: run and record the two real Ultra acceptance tasks.
- Fork defects discovered by live behavior: none yet; live evidence is not
  available, so this is not a quality claim.
