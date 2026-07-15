# coding-agents: codex

pre() {
    git-repo
    git-branch main
    requires-tool node npm
    file-exists 'docs/superpowers/plans/name-tools-plan.md'
    file-contains 'src/name-tools.js' 'nameToolsVersion'
}

post() {
    check-transcript skill-called superpowers:subagent-driven-development
    check-transcript tool-called Agent
    check-transcript tool-count Agent lte 2
    command-succeeds 'npm test'
    file-contains 'src/name-tools.js' 'export function normalizeName'
    file-contains 'src/name-tools.js' 'export function formatGreeting'
    git-count commits gte 4
}
