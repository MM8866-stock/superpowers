#!/usr/bin/env bash
# Deterministic contract test for the Ultra-first SDD controller.
# Live Agent behavior is covered by the fork eval scenarios; this test keeps
# the local harness gate fast and free of external credentials.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SKILL="$ROOT/skills/subagent-driven-development/SKILL.md"
PROMPT="$ROOT/skills/subagent-driven-development/implementer-prompt.md"

contains() { grep -Fqi -- "$2" "$1"; }
not_contains() { ! grep -Fqi -- "$2" "$1"; }

echo "=== Test: subagent-driven-development skill contracts ==="

contains "$SKILL" "scripts/sdd-workspace PLAN_FILE" \
  || { echo "FAIL: plan-scoped workspace command missing"; exit 1; }
contains "$SKILL" "at most one integrated review per milestone" \
  || { echo "FAIL: milestone review boundary missing"; exit 1; }
contains "$SKILL" "existing implementation context" \
  || { echo "FAIL: implementation-context reuse missing"; exit 1; }
contains "$SKILL" "runtime chooses each Agent's concrete model" \
  || { echo "FAIL: runtime model selection missing"; exit 1; }
contains "$PROMPT" "logical batch" \
  || { echo "FAIL: implementer logical-batch contract missing"; exit 1; }
not_contains "$SKILL" "five rounds" \
  || { echo "FAIL: fixed five-round loop leaked into SDD"; exit 1; }
not_contains "$SKILL" "rounds 4-5" \
  || { echo "FAIL: fixed escalation rounds leaked into SDD"; exit 1; }
not_contains "$SKILL" "fresh implementer per task" \
  || { echo "FAIL: per-task fresh implementer leaked into SDD"; exit 1; }
not_contains "$PROMPT" "[MODEL" \
  || { echo "FAIL: fixed model placeholder leaked into implementer prompt"; exit 1; }

echo "PASS: Ultra-first SDD contracts are present and upstream per-task semantics are absent"
