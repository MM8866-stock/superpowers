# coding-agents: codex

pre() {
    git-repo
    git-branch main
    file-contains 'src/greeting.txt' '^hello$'
    file-exists 'docs/superpowers/specs/greeting-design.md'
}

post() {
    command-succeeds 'test "$(cat src/greeting.txt)" = "hello world"'
    check-transcript tool-count Agent eq 0
    not file-exists '.superpowers/sdd/*.md'
    git-count commits gte 3
}
