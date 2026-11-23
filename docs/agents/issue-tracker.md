# Issue tracker: GitHub

Issues and specs for this repo live in the GitHub Issues tracker for the repository `johnst101/ForeTheMoney`.

Use the `gh` CLI for issue operations when it is available. This environment currently does not have the GitHub CLI installed, so the canonical workflow is documented here and should be used once `gh` is added to the local toolchain.

## Conventions

- **Create an issue**: `gh issue create --title "..." --body "..."`. Use a heredoc for multi-line bodies.
- **Read an issue**: `gh issue view <number> --json number,title,body,labels,comments`.
- **List issues**: `gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'` with appropriate `--label` and `--state` filters.
- **Comment on an issue**: `gh issue comment <number> --body "..."`.
- **Apply or remove labels**: `gh issue edit <number> --add-label "..."` / `gh issue edit <number> --remove-label "..."`.
- **Close**: post the explanation with `gh issue comment <number> --body "..."`, then `gh issue close <number>`.

Infer the repo from `git remote -v`; `gh` will use the active clone's remote when run inside the repo.

## Pull requests as a triage surface

**PRs as a request surface: no.**

When this flag is set to `yes`, PRs run through the same labels and states as issues using the `gh pr` equivalents. This repo currently treats external PRs as code review rather than as a ticketing surface, so the default is `no`.

## When a skill says "publish to the issue tracker"

Create a GitHub issue in this repository.

## When a skill says "fetch the relevant ticket"

Read the ticket using the conventions above and use the issue number to anchor research, implementation, or triage notes.
