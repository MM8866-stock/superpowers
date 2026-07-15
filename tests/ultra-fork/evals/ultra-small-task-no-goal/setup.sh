#!/usr/bin/env bash
set -euo pipefail

setup-helpers run create_base_repo
mkdir -p src docs/superpowers/specs
printf 'hello\n' > src/greeting.txt
cat > docs/superpowers/specs/greeting-design.md <<'EOF'
# Greeting Design

Delivery maturity: internal V1.

Replace the single line in `src/greeting.txt` with `hello world`. No other
behavior or file changes are required.
EOF
git add src/greeting.txt docs/superpowers/specs/greeting-design.md
git commit -m "test: add approved greeting fixture" --quiet
