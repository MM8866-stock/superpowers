#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
evals_root="$repo_root/evals"
overlay_root="$repo_root/tests/ultra-fork/evals"
evals_repo="https://github.com/prime-radiant-inc/superpowers-evals.git"

scenario_names=(
  ultra-small-task-no-goal
  ultra-logical-batch-plan
  ultra-sdd-context-reuse
  ultra-wait-timeout-not-blocked
  ultra-v1-review-boundary
  ultra-final-scope-map
)

mode="install"
if [ $# -gt 1 ]; then
  echo "usage: $0 [--check]" >&2
  exit 2
fi
if [ $# -eq 1 ]; then
  [ "$1" = "--check" ] || { echo "usage: $0 [--check]" >&2; exit 2; }
  mode="check"
fi

if [ -d "$evals_root/.git" ]; then
  : # Reuse the existing checkout; never replace local eval results or state.
elif [ -e "$evals_root" ]; then
  echo "$evals_root exists but is not a git checkout" >&2
  exit 1
else
  git clone --depth 1 "$evals_repo" "$evals_root"
fi

for scenario in "${scenario_names[@]}"; do
  source_dir="$overlay_root/$scenario"
  target_dir="$evals_root/scenarios/$scenario"
  [ -d "$source_dir" ] || { echo "missing overlay: $source_dir" >&2; exit 1; }
  mkdir -p "$target_dir"
  cp "$source_dir/story.md" "$source_dir/setup.sh" "$source_dir/checks.sh" "$target_dir/"
  chmod +x "$target_dir/setup.sh"
  chmod -x "$target_dir/checks.sh"
done

export SUPERPOWERS_ROOT="$repo_root"

if command -v bun >/dev/null 2>&1; then
  bun_bin="$(command -v bun)"
elif [ -x "$HOME/.bun/bin/bun" ]; then
  bun_bin="$HOME/.bun/bin/bun"
else
  echo "bun >= 1.3.13 is required: https://bun.sh" >&2
  exit 1
fi
export PATH="$(dirname "$bun_bin"):$PATH"

if [ ! -d "$evals_root/node_modules" ]; then
  (cd "$evals_root" && "$bun_bin" install)
fi

if [ "$mode" = "check" ]; then
  scenario_args=()
  for scenario in "${scenario_names[@]}"; do
    scenario_args+=("scenarios/$scenario")
  done
  (cd "$evals_root" && "$bun_bin" run quorum check "${scenario_args[@]}")
else
  printf 'Installed %d fork scenarios into %s\n' "${#scenario_names[@]}" "$evals_root/scenarios"
  printf 'Run %s --check before any live evaluation.\n' "$0"
fi
