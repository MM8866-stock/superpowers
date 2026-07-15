#!/usr/bin/env bash
set -euo pipefail

setup-helpers run create_base_repo
mkdir -p docs/superpowers/specs
cat > docs/superpowers/specs/contact-import-design.md <<'EOF'
# Contact Import Design

## Delivery Maturity

Internal V1. Correct local imports are required. Network retries, telemetry,
and multi-user concurrency are follow-up hardening.

## Approved Scope

R1. Parse a UTF-8 CSV stream into `{name, email}` records. Reject a row that
does not contain exactly two non-empty fields.

R2. Save all parsed records atomically to a local JSON repository; validation
failure leaves the prior file unchanged.

R3. Add an `import-contacts <csv> <json>` CLI command that reports the imported
record count and returns non-zero on parser or storage failure.

## Architecture

Keep parser, repository, and CLI orchestration behind stable interfaces. Use
focused tests for each contract and one CLI integration check.
EOF
git add docs/superpowers/specs/contact-import-design.md
git commit -m "docs: add approved contact import design" --quiet
