# Ultra-first Superpowers Fork

## Identity

- Upstream: `obra/superpowers`
- Maintained fork: `MM8866-stock/superpowers`
- Initial upstream baseline: `v6.1.1` / `d884ae04edebef577e82ff7c4e143debd0bbec99`
- Plugin and Skill namespace: unchanged (`superpowers`, `superpowers:*`)
- Fork release convention: `<upstream-version>-ultra.<fork-release>`

The fork replaces the official installation. The official and forked plugins must not be enabled together.

## Purpose

This fork retains Superpowers' design, TDD, debugging, verification, and branch-finishing discipline while making long-running engineering work proportionate to GPT-5.6 Ultra and modern Codex runtimes.

The core differences are:

- one delivery-maturity decision during brainstorming;
- logical implementation batches instead of mechanical micro-steps;
- small work completed directly without a large Goal workflow;
- Agent dispatch based on purpose and net benefit, not available capacity;
- healthy implementation context reused within a Goal, responsibility domain, and logical batch;
- runtime-selected model and reasoning level within the user's configured ceiling;
- one shared-workspace writer unless isolated worktrees and stable ownership make parallel writes safe;
- integrated milestone review instead of review after every Task;
- focused, module, milestone, and final validation layers;
- wait timeouts treated as missing updates rather than proof of blockage;
- root-cause convergence instead of fixed time, Token, or retry fuses;
- a seven-field Goal ledger updated only at durable recovery boundaries.

## Non-goals

The fork does not add an external scheduler, model router, Agent database, management UI, automatic Agent termination, distributed locks, heartbeat takeover, fixed Sol/Terra/Luna routing, Cursor dynamic scheduling, or Claude Code dynamic model routing.

## Upstream Maintenance

`upstream/dev` is observed for evidence, not merged automatically. Each stable upstream release receives a semantic diff review. Security fixes and high-value Codex compatibility fixes may be cherry-picked early after focused verification.

Fork behavior is protected by three layers:

1. deterministic Skill and monitor contracts;
2. sequential normal Codex scenarios using the current subscription runtime;
3. a small set of real GPT-5.6 Ultra acceptance tasks for major SDD or runtime changes.

Upstream monitoring records stable releases, `dev`, the evaluation repository, relevant Issue/PR updates, and high-value path changes without model calls. A separate Codex automation summarizes important changes in Simplified Chinese once per day and never modifies the fork automatically.
