# Create Plan

Create a new numbered implementation plan in `docs/plans/` and update the plan index.

## Inputs

- Goal and scope from caller: `$ARGUMENTS`

## Required Context

- Read `docs/plans/README.md`.
- Read `docs/design/README.md`.
- Read related feature specs in `docs/features/` if available.
- Read `AGENTS.md`.

## Interaction

Ask concise follow-up questions only when scope, constraints, or success criteria are unclear.

## Output

Create `docs/plans/NNN-<kebab-title>.md` with:

- Title and status (`PROPOSED` initially)
- Date fields
- Context
- Goals
- Non-goals
- Phases
- Deliverables and outcomes
- Risks/unknowns
- Verification approach

Then update `docs/plans/README.md`:

- Add plan to current focus if active.
- Update next steps accordingly.

## Plan File Template

```markdown
# NNN - <Title>

Status: PROPOSED
Created: YYYY-MM-DD
Updated: YYYY-MM-DD

## Context

## Goals

- ...

## Non-goals

- ...

## Phases

- Phase 1 - ...
- Phase 2 - ...

## Outcomes

- ...

## Verification

- ...
```
