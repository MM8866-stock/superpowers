# coding-agents: codex

pre() {
    git-repo
    git-branch main
    file-exists 'docs/superpowers/specs/contact-import-design.md'
    not file-exists 'docs/superpowers/plans/*.md'
}

post() {
    file-exists 'docs/superpowers/plans/*.md'
    command-succeeds 'plan=$(find docs/superpowers/plans -maxdepth 1 -name "*.md" -type f | head -1); grep -q "contact-import-design.md" "$plan"'
    command-succeeds 'plan=$(find docs/superpowers/plans -maxdepth 1 -name "*.md" -type f | head -1); count=$(grep -cE "^### Task [0-9]+:" "$plan"); test "$count" -ge 2 && test "$count" -le 4'
    command-succeeds '! grep -R -E "2-5 minutes|Each step is one action" docs/superpowers/plans'
    command-succeeds 'test ! -d src && test ! -d test && test ! -d tests'
}
