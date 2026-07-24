#!/usr/bin/env bash
# Deterministic integration gate for the Ultra-first SDD workflow.
# Live Agent scenarios run through the fork's eval overlay; this gate verifies
# the plan-scoped plumbing and local contracts without external credentials.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=== Integration Test: Ultra-first subagent-driven-development ==="
"$SCRIPT_DIR/test-subagent-driven-development.sh"
"$SCRIPT_DIR/test-sdd-workspace.sh"
"$ROOT/tests/ultra-fork/run-tests.sh"

echo "PASS: SDD workspace, controller, and fork contracts integrate cleanly"
