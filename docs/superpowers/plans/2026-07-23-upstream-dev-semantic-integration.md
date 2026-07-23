# Upstream Dev Semantic Integration Implementation Plan

> **For agentic workers:** Follow the approved spec and repository instructions. Use superpowers:subagent-driven-development for an approved large Goal, or superpowers:executing-plans for inline execution.

**Goal:** Integrate `upstream/dev` at `cc690476fca428d124544e74145ed91dfb10f8e3` while preserving the Ultra-first fork's tested behavior.

**Architecture:** Record upstream as a real merge parent, then resolve conflicts by semantic ownership rather than by choosing one side wholesale. Deterministic fork contracts define the protected behavior; upstream runtime, portability, workspace, packaging, and documentation changes are adopted where they compose with those contracts.

**Tech Stack:** Git, Bash, Python `unittest`, Node.js, JSON plugin manifests, Markdown Skills

**Approved Spec:** [`docs/superpowers/specs/2026-07-23-upstream-dev-semantic-integration-design.md`](../specs/2026-07-23-upstream-dev-semantic-integration-design.md)

## Global Constraints

- Preserve the `superpowers` plugin name and `superpowers:*` Skill namespace.
- Keep reusable prose, prompts, tests, and maintenance documents in English.
- Add no dependency, provider key, project-specific path, fixed model matrix, or external scheduler.
- Preserve the fork contracts listed in the approved spec and `docs/ultra-fork.md`.
- Keep `origin/main` as first parent and the pinned `upstream/dev` SHA as second parent.
- Do not push or update GitHub `main` in this plan.

---

### Task 1: Lock the Composed Fork Contracts

**Spec:** `docs/superpowers/specs/2026-07-23-upstream-dev-semantic-integration-design.md`, sections `Protected Fork Semantics` and `Testing`

**Outcome:** Deterministic tests describe the upstream improvements that the fork will accept together with the Ultra behavior that must remain.

**Files:**
- Modify: `tests/ultra-fork/test_skill_contracts.py`
- Test: `tests/ultra-fork/test_skill_contracts.py`

**Interfaces:**
- Consumes: current fork Skill and SDD helper file layout
- Produces: integration contracts for plan-scoped SDD workspaces, scoped fix rechecks, runtime-selected scheduling, milestone review, and absence of fixed-round/per-task review semantics

**Acceptance behavior:**
- Contracts require `sdd-workspace PLAN_FILE` to isolate artifacts by plan.
- Contracts require resumable, scoped review-fix continuation without a fixed five-round breaker or forced fresh Agent/model escalation.
- Existing delivery maturity, logical-batch planning, seven-field ledger, single-writer, context-reuse, and runtime scheduling contracts remain unchanged.
- The new tests fail against the pre-integration tree only because accepted upstream behavior is absent.

**Implementation notes:**
- Test observable phrases, file existence, and helper behavior; do not pin full prose or implementation formatting.
- Reuse the existing `read_text` helper and temporary Git repository patterns from upstream SDD workspace tests where appropriate.

**Focused verification:**
- RED: `python3 -m unittest tests.ultra-fork.test_skill_contracts -v` — expected failure: plan-scoped workspace and scoped re-review integration behavior are missing.
- GREEN: `tests/ultra-fork/run-tests.sh` — expected: PASS after Tasks 2 and 3.
- Batch check: `git diff --check` — expected: PASS.

**Commit:**

`git commit -m "test: lock upstream dev integration contracts"`

### Task 2: Integrate Generic Upstream Runtime And Packaging Changes

**Spec:** `docs/superpowers/specs/2026-07-23-upstream-dev-semantic-integration-design.md`, section `Integration Strategy`

**Outcome:** The branch records the pinned upstream merge parent and adopts non-SDD portability, hook, packaging, manifest, harness, and documentation improvements without losing fork identity.

**Files:**
- Modify: `.claude-plugin/marketplace.json`
- Modify: `.claude-plugin/plugin.json`
- Modify: `.codex-plugin/plugin.json`
- Modify: `.cursor-plugin/plugin.json`
- Modify: `.kimi-plugin/plugin.json`
- Modify: `gemini-extension.json`
- Modify: `package.json`
- Modify: `hooks/hooks.json`
- Delete: `hooks/session-start-codex`
- Modify: `scripts/package-codex-plugin.sh`
- Modify: `tests/codex/test-package-codex-plugin.sh`
- Modify: `tests/codex/test-marketplace-manifest.sh`
- Modify: `tests/hooks/test-session-start.sh`
- Modify: `docs/windows/polyglot-hooks.md`
- Modify: `docs/porting-to-a-new-harness.md`
- Modify: `CLAUDE.md`
- Modify: `README.md`
- Modify: `RELEASE-NOTES.md`
- Create: `docs/superpowers/plans/2026-07-06-sdd-plan-scoped-workspace.md`
- Create: `docs/superpowers/plans/2026-07-15-sdd-fix-loop-redesign.md`
- Create: `docs/superpowers/specs/2026-07-06-sdd-plan-scoped-workspace-eval-results.md`
- Create: `docs/superpowers/specs/2026-07-06-sdd-plan-scoped-workspace.md`
- Create: `docs/superpowers/specs/2026-07-15-sdd-fix-loop-redesign-design.md`

**Interfaces:**
- Consumes: upstream hook dispatch and Codex portal archive contracts; fork version and repository identity
- Produces: portable Bash packaging, explicit empty Codex hooks metadata, Windows Git Bash SessionStart dispatch, and manifests that retain the `6.1.1-ultra.1` fork version

**Acceptance behavior:**
- `git rev-parse HEAD^2` resolves to the pinned upstream SHA after the final merge commit.
- Fork-owned identity, tracking, eval overlay, and monitor files are preserved.
- Packaging works on GNU/Linux without BSD-specific tar assumptions and emits the fork version.
- Hook tests confirm Windows Bash dispatch while Codex portal metadata does not rediscover removed hooks.

**Implementation notes:**
- Start `git merge --no-ff --no-commit upstream/dev`, then resolve this batch and Task 3 before creating the single merge commit.
- For add/add packaging conflicts, reconcile the fork's newer archive behavior with upstream portability fixes; do not choose either file wholesale without diff review.
- Leave Skill conflicts unresolved until Task 3.

**Focused verification:**
- GREEN: `tests/codex/test-package-codex-plugin.sh` — expected: PASS.
- GREEN: `tests/codex/test-marketplace-manifest.sh` — expected: PASS.
- GREEN: `tests/hooks/test-session-start.sh` — expected: PASS.
- Batch check: `tests/antigravity/run-tests.sh && tests/kimi/run-tests.sh` — expected: PASS.

**Commit:**

This batch remains staged inside the pending merge and is committed with Task 3 as the single merge commit.

### Task 3: Reconcile Skills And Complete The Semantic Merge

**Spec:** `docs/superpowers/specs/2026-07-23-upstream-dev-semantic-integration-design.md`, sections `Integration Strategy`, `Protected Fork Semantics`, and `Acceptance Criteria`

**Outcome:** Upstream plan-scoped workspace and scoped fix-loop improvements compose with the fork's delivery-proportionate SDD controller, and the completed merge passes local verification.

**Files:**
- Modify: `skills/brainstorming/SKILL.md`
- Modify: `skills/brainstorming/visual-companion.md`
- Modify: `skills/dispatching-parallel-agents/SKILL.md`
- Modify: `skills/executing-plans/SKILL.md`
- Modify: `skills/finishing-a-development-branch/SKILL.md`
- Modify: `skills/receiving-code-review/SKILL.md`
- Modify: `skills/requesting-code-review/SKILL.md`
- Modify: `skills/subagent-driven-development/SKILL.md`
- Modify: `skills/subagent-driven-development/implementer-prompt.md`
- Create: `skills/subagent-driven-development/re-review-prompt.md`
- Delete: `skills/subagent-driven-development/task-reviewer-prompt.md`
- Modify: `skills/subagent-driven-development/scripts/sdd-workspace`
- Modify: `skills/subagent-driven-development/scripts/review-package`
- Modify: `skills/subagent-driven-development/scripts/task-brief`
- Modify: `skills/systematic-debugging/SKILL.md`
- Modify: `skills/test-driven-development/SKILL.md`
- Delete: `skills/test-driven-development/testing-anti-patterns.md`
- Create: `skills/test-driven-development/writing-good-tests.md`
- Modify: `skills/using-git-worktrees/SKILL.md`
- Modify: `skills/using-superpowers/references/codex-tools.md`
- Create: `skills/using-superpowers/references/gemini-tools.md`
- Modify: `skills/verification-before-completion/SKILL.md`
- Modify: `skills/writing-plans/SKILL.md`
- Modify: `skills/writing-skills/SKILL.md`
- Modify: `docs/ultra-fork.md`
- Modify: `tests/antigravity/test-antigravity-tools.sh`
- Modify: `tests/claude-code/run-skill-tests.sh`
- Modify: `tests/claude-code/test-helpers.sh`
- Modify: `tests/claude-code/test-sdd-workspace.sh`
- Modify: `tests/claude-code/test-subagent-driven-development.sh`
- Modify: `tests/pi/test-pi-extension.mjs`

**Interfaces:**
- Consumes: Task 1 contracts, upstream plan-scoped helper CLI, existing milestone reviewer and seven-field Goal ledger
- Produces: plan-scoped scratch artifacts plus resumable scoped fix verification within the fork's milestone-based controller

**Acceptance behavior:**
- `sdd-workspace` requires one plan path, derives an isolated plan slug, and keeps all scratch state ignored.
- A healthy Implementer remains reusable for fixes; a fresh Agent or stronger model is selected only by runtime judgment, not a fixed round number.
- Re-review receives only named findings and the fix diff, and cannot expand into a fresh broad review.
- Per-task mandatory reviews, fixed five-round breakers, fixed model tiers, and upstream task reviewer prompts remain absent.
- The merge commit has the required two parents and the worktree is clean.

**Implementation notes:**
- Resolve Skill conflicts from the fork version outward, adding only upstream concepts that satisfy Task 1 contracts.
- Preserve upstream authorship in Git history through the merge parent; document intentionally deferred incompatible SDD controller semantics in the merge commit body or release notes.
- Do not weaken an existing fork contract merely to make upstream tests pass; adapt tests whose assumptions deliberately differ in the fork.

**Focused verification:**
- GREEN: `tests/ultra-fork/run-tests.sh` — expected: PASS.
- GREEN: `tests/claude-code/test-sdd-workspace.sh` — expected: PASS.
- GREEN: `tests/claude-code/test-subagent-driven-development.sh` — expected: PASS.
- GREEN: `tests/antigravity/run-tests.sh && tests/opencode/run-tests.sh && tests/kimi/run-tests.sh` — expected: PASS.
- GREEN: `node --test tests/brainstorm-server/*.test.js` — expected: PASS.
- Static eval check: `scripts/install-fork-evals.sh --check` — expected: PASS or a clearly attributed external-tool prerequisite failure.
- Final check: `git diff --check HEAD^1 HEAD && git status --short --branch && test "$(git rev-parse HEAD^2)" = "cc690476fca428d124544e74145ed91dfb10f8e3"` — expected: clean, exact second parent.

**Commit:**

`git commit -m "merge: integrate upstream dev semantically"`
