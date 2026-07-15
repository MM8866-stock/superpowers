# coding-agents: codex

pre() {
    git-repo
    git-branch main
    requires-tool node npm
    file-exists 'docs/superpowers/plans/url-tools-plan.md'
    not file-exists 'docs/superpowers/evidence/final-scope-map.md'
}

post() {
    check-transcript skill-called superpowers:subagent-driven-development
    command-succeeds 'npm test'
    file-contains 'src/url-tools.js' 'export function slugify'
    file-contains 'src/url-tools.js' 'export function makeUrl'
    file-exists 'docs/superpowers/evidence/final-scope-map.md'
    file-contains 'docs/superpowers/evidence/final-scope-map.md' 'R1'
    file-contains 'docs/superpowers/evidence/final-scope-map.md' 'R2'
    file-contains 'docs/superpowers/evidence/final-scope-map.md' '[0-9a-f]{7,40}'
    file-contains 'docs/superpowers/evidence/final-scope-map.md' 'npm test'
}
