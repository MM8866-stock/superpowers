# coding-agents: codex

pre() {
    git-repo
    git-branch main
}

post() {
    check-transcript tool-count Agent eq 1
    check-transcript tool-count wait_agent gte 2
    check-transcript tool-not-called wait
    file-exists 'delayed.txt'
    command-succeeds 'test "$(cat delayed.txt)" = "DELAY_OK"'
}
