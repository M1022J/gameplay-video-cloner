# Collaboration, Git, And Delegation

## Git Hygiene

- One logical change per commit.
- Use present-tense imperative commit subjects: `Add caching`, not `Added
  caching`.
- Keep the first line short, typically <= 50 characters.
- Add a blank line before details.
- Follow project commit templates when present.
- Do not include agent/tool prefixes in commit, PR, issue, or doc titles.
- Do not commit secrets, generated credentials, or local machine paths.

When working as an agent:

- Do not commit until the user approves the exact diff.
- Do not push, tag, or open/update PRs until the user approves that remote
  action.
- Approval to commit is local-only unless push approval is explicit.
- Approval to open/update a PR does not imply approval to create new commits.

## PR Hygiene

- Use the repository's PR template when present.
- Describe what changed and how it was verified.
- Do not use PR descriptions as a dump of automated test logs.
- List manual validation only when it actually happened.
- Keep titles direct and artifact-free.
- Review the whole change before leaving comments.
- Prioritize findings by severity and file/line.

## Delegation

Implement directly by default. Delegate only when it pays for itself:

- two or more independent workstreams can run in parallel
- the task produces very noisy output that would crowd context
- the change is large, mechanical, and well specified
- isolation is useful for an independent read or verification pass

Keep these in the main thread:

- architecture
- module boundaries
- public APIs
- schemas and wire contracts
- concurrency model
- error contract
- final review and verification

When delegating:

- state goal, constraints, acceptance criteria, files in/out of scope
- specify the contract, not the implementation
- avoid duplicate work between agents
- verify at the contract boundary

