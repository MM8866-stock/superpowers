#!/usr/bin/env bash
set -euo pipefail

setup-helpers run create_base_repo
mkdir -p src test docs/superpowers/specs docs/superpowers/plans
cat > package.json <<'EOF'
{
  "name": "url-tools-eval",
  "version": "1.0.0",
  "type": "module",
  "scripts": {"test": "node --test"}
}
EOF
cat > src/url-tools.js <<'EOF'
export const urlToolsVersion = 1;
EOF
cat > docs/superpowers/specs/url-tools-design.md <<'EOF'
# URL Tools Design

R1. `slugify(value)` trims input, lowercases ASCII letters, replaces each run
of non-alphanumeric characters with one hyphen, and removes outer hyphens.

R2. `makeUrl(base, title)` removes trailing slashes from `base` and appends
`/` plus `slugify(title)`. Reject an empty slug with `Error("title is required")`.
EOF
cat > docs/superpowers/plans/url-tools-plan.md <<'EOF'
# URL Tools Implementation Plan

Approved spec: `docs/superpowers/specs/url-tools-design.md`.

## Milestone 1: URL Tools

### Task 1: R1 Slug Contract
Implement and test `slugify` with focused RED/GREEN evidence and one commit.

### Task 2: R2 URL Contract
Continue the responsibility, implement and test `makeUrl`, and commit it.

Milestone gate: `npm test`. Finish with a requirement-to-commit-and-verification
mapping for R1 and R2.
EOF
git add package.json src docs
git commit -m "test: add URL tools evidence fixture" --quiet
