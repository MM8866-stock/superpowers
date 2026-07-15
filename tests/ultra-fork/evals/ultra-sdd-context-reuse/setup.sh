#!/usr/bin/env bash
set -euo pipefail

setup-helpers run create_base_repo
mkdir -p src test docs/superpowers/specs docs/superpowers/plans
cat > package.json <<'EOF'
{
  "name": "name-tools-eval",
  "version": "1.0.0",
  "type": "module",
  "scripts": {"test": "node --test"}
}
EOF
cat > src/name-tools.js <<'EOF'
export const nameToolsVersion = 1;
EOF
cat > docs/superpowers/specs/name-tools-design.md <<'EOF'
# Name Tools Design

Internal V1. `normalizeName(value)` trims outer whitespace and collapses each
internal whitespace run to one space. `formatGreeting(value)` returns
`Hello, <normalized>!` and reuses `normalizeName`. Empty normalized names are
rejected with `Error("name is required")`.
EOF
cat > docs/superpowers/plans/name-tools-plan.md <<'EOF'
# Name Tools Implementation Plan

**Approved Spec:** `docs/superpowers/specs/name-tools-design.md`

## Milestone 1: Name Tools

### Task 1: Normalization Contract

Outcome: implement and test `normalizeName` in `src/name-tools.js` using focused
RED/GREEN evidence. Commit the coherent behavior.

### Task 2: Greeting Contract

Outcome: continue the same responsibility area, implement and test
`formatGreeting`, reuse `normalizeName`, and commit the coherent behavior.

Milestone verification: `npm test`. One integrated review at the milestone.
EOF
git add package.json src docs
git commit -m "test: add name tools SDD fixture" --quiet
