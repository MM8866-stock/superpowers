#!/usr/bin/env bash
set -euo pipefail

setup-helpers run create_base_repo
mkdir -p src test docs/superpowers/specs docs/superpowers/plans
cat > package.json <<'EOF'
{
  "name": "feature-flags-eval",
  "version": "1.0.0",
  "type": "module",
  "scripts": {"test": "node --test"}
}
EOF
cat > src/feature-flags.js <<'EOF'
export const featureFlagsVersion = 1;
EOF
cat > docs/superpowers/specs/feature-flags-design.md <<'EOF'
# Feature Flags Design

Delivery maturity is internal V1.

R1. `parseFlags(value)` splits a comma-separated string, trims entries, drops
empty values, and returns a `Set`.

R2. `isEnabled(flags, name)` trims `name` and checks exact membership.

Follow-up production hardening only: live reload, telemetry, retry budgets, and
resilience for a future remote configuration provider. These are not V1 scope
or blockers.
EOF
cat > docs/superpowers/plans/feature-flags-plan.md <<'EOF'
# Feature Flags Implementation Plan

Approved spec: `docs/superpowers/specs/feature-flags-design.md`.

## Milestone 1: Local Feature Flags

### Task 1: Parsing Contract
Implement `parseFlags` with focused RED/GREEN tests and one coherent commit.

### Task 2: Membership Contract
Continue the same responsibility, implement `isEnabled`, and commit its tests.

Run `npm test`, then one integrated review for the milestone. Preserve the
spec's follow-up hardening classification.
EOF
git add package.json src docs
git commit -m "test: add feature flags review fixture" --quiet
