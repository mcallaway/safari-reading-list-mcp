# Close Plan

Finalize an active plan before merge.

## Inputs

- Plan identifier or title from caller: `$ARGUMENTS`

## Required Context

- Read the target plan file in `docs/plans/`.
- Read `docs/plans/README.md`.
- Read `docs/design/README.md`.
- Scan `docs/decisions/` for related ADR drafts.

## Process

- Verify all planned phases and outcomes are complete.
- Update plan status to `COMPLETE` and completion date.
- Update `docs/plans/README.md`:
  - move items from current focus to recent work,
  - refresh next steps.
- Confirm design docs reflect final implementation.
- Finalize or explicitly defer ADR drafts.
- Flag remaining loose ends clearly.

## Output

- A concise closure report listing:
  - completed outcomes,
  - deferred items,
  - documentation updates made.
- Commit with message:
  - `docs: close plan NNN -- <title>`
