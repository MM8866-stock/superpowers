## Subagent dispatch requires multi-agent support

Add to your Codex config (`~/.codex/config.toml`):

```toml
[features]
multi_agent = true
```

This enables `spawn_agent`, `wait_agent`, and `close_agent` for skills like `dispatching-parallel-agents` and `subagent-driven-development`.

## Ultra-Native Scheduling

Codex Ultra-native scheduling is a capable runtime that may choose useful Agent
roles, concurrency, models, and reasoning levels. It still reads and follows
project and Skill constraints; those constraints provide purpose and safety
boundaries rather than a fixed external scheduler.

- The runtime chooses concrete child models and reasoning levels within the
  parent task's configured ceiling.
- If child selection is unavailable, inherit the parent configuration instead
  of claiming an unverified upgrade or downgrade.
- Do not create Agents merely because capacity is available.
- Do not interrupt valid Agent work solely for imperfect strategy compliance;
  correct future instructions unless the work is conflicting, unsafe, failed,
  cancelled, or no longer useful.

## Waiting And Agent Lifecycle

- A `wait_agent` timeout means **no update yet**, not failure. Elapsed time alone
  does not establish that an Agent is blocked.
- Continue a healthy Agent thread during the same run when it retains useful
  context for the same Goal and responsibility. Across a new run or app restart,
  recover from Git and durable artifacts instead of assuming the thread exists.
- Use `close_agent` at a natural lifecycle boundary: completed responsibility,
  explicit failure, cancellation, or no remaining purpose. Do not close an
  Implementer after one logical batch when immediate continuation benefits from
  its context.
- A queued message is not necessarily an immediate Agent turn. Use the runtime's
  supported follow-up mechanism when a response or additional action is needed.

## Environment Detection

Skills that create worktrees or finish branches should detect their
environment with read-only git commands before proceeding:

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
BRANCH=$(git branch --show-current)
```

- `GIT_DIR != GIT_COMMON` → already in a linked worktree (skip creation)
- `BRANCH` empty → detached HEAD (cannot branch/push/PR from sandbox)

See `using-git-worktrees` Step 0 and `finishing-a-development-branch`
Step 1 for how each skill uses these signals.

## Codex App Finishing

When the sandbox blocks branch/push operations (detached HEAD in an
externally managed worktree), the agent commits all work and informs
the user to use the App's native controls:

- **"Create branch"** — names the branch, then commit/push/PR via App UI
- **"Hand off to local"** — transfers work to the user's local checkout

The agent can still run tests, stage files, and output suggested branch
names, commit messages, and PR descriptions for the user to copy.
