# Start Work

Load project context for an implementation session.

## Inputs

- Optional task/phase focus from caller: `$ARGUMENTS`

## Required Context

- Read `docs/plans/README.md` to find active plan.
- Read active plan file in `docs/plans/`.
- Read root `AGENTS.md`.
- Read relevant directory instructions:
  - `docs/AGENTS.md` when touching docs.
  - `.github/prompts/AGENTS.md` when touching prompts.
- Read related feature or design docs as needed.

## Output: Session Context Report

Produce:

- Active plan and status
- Current phase and explicit task candidates
- Relevant design/decision context
- Preconditions and dependency checks
- Recommended first concrete edit

## Interaction

Ask: "Which phase/task are you executing in this session?"
