# Code Review

Perform a human-oriented review of repository changes with this priority order: correctness, clarity, concision, maintainability.

## Inputs

- Optional scope from caller: `$ARGUMENTS`

## Required Context

- Read `AGENTS.md`.
- Read relevant directory instructions:
  - `docs/AGENTS.md` if docs changed.
  - `.github/prompts/AGENTS.md` if prompts changed.
- Inspect changed files (`git status`, `git diff --stat`, then targeted diffs).

## Review Checklist

- Correctness:
  - Does behavior match intended outcomes?
  - Are edge cases and failure paths handled?
- Consistency with conventions:
  - Does code and docs follow `AGENTS.md` guidance?
  - Are naming and structure consistent with existing patterns?
- Code quality:
  - Is logic easy to understand?
  - Is duplication avoidable?
  - Are interfaces explicit and minimal?
- Security and safety:
  - Any unsafe shell execution, unchecked input, or secret leakage?
  - Any platform assumptions that break macOS Safari workflows?

## Commands to Run

- `uv run python -m compileall .`
- `uv run python main.py`

If review scope includes only docs, skip runtime checks and validate markdown links/consistency.

## Output Format

- Summary
- Critical issues (must-fix)
- Improvements (should-fix)
- Observations (nice-to-have)

## Review Rules

- Do not rewrite entire files unless explicitly requested.
- Do not praise routine competence.
- Keep review shorter than the changed code volume.
