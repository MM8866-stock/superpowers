# coding-agents: codex

pre() {
    git-repo
    git-branch main
    requires-tool node npm
    file-exists 'docs/superpowers/plans/feature-flags-plan.md'
}

post() {
    check-transcript skill-called superpowers:subagent-driven-development
    check-transcript tool-called Agent
    check-transcript tool-count Agent lte 2
    command-succeeds 'npm test'
    file-contains 'src/feature-flags.js' 'export function parseFlags'
    file-contains 'src/feature-flags.js' 'export function isEnabled'
    not file-contains 'src/feature-flags.js' 'telemetry|retry|remote|reload'
}
