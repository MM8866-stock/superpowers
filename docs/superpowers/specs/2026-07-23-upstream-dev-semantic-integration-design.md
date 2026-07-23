# Upstream Dev Semantic Integration Design

## Context

The Ultra-first fork is based on upstream `v6.1.1` and normally observes
`upstream/dev` without merging it. The fork owner has explicitly requested a
one-time integration of `upstream/dev` at
`cc690476fca428d124544e74145ed91dfb10f8e3`.

The upstream range changes SDD lifecycle behavior, plan-scoped workspace
handling, Windows hook dispatch, Codex packaging, tests, and supporting Skill
prose. Several of those paths also contain deliberate Ultra-first behavior, so
a blind merge result is not acceptable.

## Integration Strategy

Create a merge commit with `origin/main` as the first parent and the requested
`upstream/dev` tip as the second parent. Resolve the merge by semantic area:

1. Adopt upstream runtime, portability, hook, packaging, documentation, and
   test fixes when they do not contradict fork policy.
2. Reconcile SDD and planning changes against the fork contracts rather than
   selecting either side wholesale.
3. Preserve fork-owned monitoring, evaluation overlays, identity documents,
   version convention, and tracking state.
4. Keep upstream copyright, license, authorship, and acknowledgements intact.

The merge is prepared on `codex/merge-upstream-dev`. It is not pushed and does
not update GitHub `main` without review of the complete diff.

## Protected Fork Semantics

The integrated result must retain these observable contracts:

- delivery maturity is decided once and non-blocking hardening is deferred;
- plans use logical, independently verifiable batches;
- Agent dispatch requires a concrete purpose and positive net benefit;
- healthy implementation context may be reused within a Goal and responsibility;
- runtime scheduling chooses models and reasoning within the configured ceiling;
- shared-workspace writes remain single-writer unless isolation is explicit;
- review occurs at meaningful milestones rather than mechanically per task;
- verification remains layered and failures converge by root cause;
- wait timeouts are not treated as proof of failure;
- Goal state keeps the fork's durable seven-field ledger contract.

Upstream SDD workspace and bounded fix-loop improvements may be adopted only
where they compose with these contracts. Fixed per-task fresh Agents, mandatory
per-task review fanout, fixed model routing, or hard time/token fuses must not
be reintroduced.

## Testing

Before integration, run `tests/ultra-fork/run-tests.sh` as the baseline. During
conflict resolution, add or tighten deterministic contracts before changing a
protected behavior that is not already covered, and observe the expected RED
failure before the corresponding Skill edit.

After integration, run:

- `tests/ultra-fork/run-tests.sh`;
- affected SDD, hook, Codex packaging, and harness test suites;
- the repository's remaining local plugin test suites;
- static fork evaluation installation with `scripts/install-fork-evals.sh --check`.

Normal Codex and real Ultra evaluations are milestone gates. They are required
only if deterministic reconciliation changes the fork's intended SDD behavior,
not for a merge that preserves the existing contracts byte-for-byte in meaning.

## Acceptance Criteria

- Git history records the exact upstream `dev` tip as a merge parent.
- All non-conflicting generic upstream improvements are present.
- Ultra-first contracts and fork-owned files remain valid.
- Focused and repository-wide local verification passes.
- The final diff and any deferred upstream behavior are documented for human
  review before push or main-branch integration.
