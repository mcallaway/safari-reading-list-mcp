# Review PR

Perform a pre-merge pull request readiness check.

## Inputs

- PR number/url or scope from caller: `$ARGUMENTS`

## Process

- Check local git state (`git status --short`, branch, uncommitted changes).
- Inspect PR metadata (`gh pr view` when available).
- Review changed files and diff summary.
- Check documentation sync (`docs/`, `AGENTS.md`, prompts as applicable).
- Run practical quality checks for this repo:
  - `uv run python -m compileall .`
  - `uv run python main.py`

## Output

Provide:

- Status table:
  - Local state
  - CI/check status (if available)
  - Mergeability
  - Review completeness
- Concerns and blocking issues
- Verdict:
  - `ready to merge`
  - or `blocked by <issue list>`

If `gh` is unavailable, continue with local-only review and state that limitation explicitly.
