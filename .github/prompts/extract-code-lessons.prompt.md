# Extract Code Lessons

Extract durable engineering lessons from recent repository history and write them to `docs/guides/`.

## Inputs

- Optional time window or topic from caller: `$ARGUMENTS`

## Default Scope

- Last 7 days of commits if no scope is provided.

## Required Context

- Read `AGENTS.md`.
- Read relevant docs under `docs/design/` and `docs/decisions/`.
- Analyze git history and diffs for selected time period.

## Analysis Categories

- Architecture and design choices
- Implementation techniques
- Refactoring and evolution patterns
- Mistakes and corrections

## Output

Write a new guide in `docs/guides/` named:

- `lessons-YYYY-MM-DD.md` (or caller-provided name)

Include:

- concise lesson statements,
- supporting code excerpts or commit references,
- recommended promotion of lessons into `AGENTS.md`, design docs, or ADRs when appropriate.

Do not return lessons only in chat; persist them in repository docs.
