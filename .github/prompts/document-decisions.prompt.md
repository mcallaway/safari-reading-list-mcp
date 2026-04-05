# Document Decisions

Capture implementation trade-offs and route them to the right documentation artifact.

## Inputs

- Decision summary from caller: `$ARGUMENTS`

## Required Context

- Read `docs/design/README.md`.
- Read `docs/decisions/README.md`.
- Read related plan/design/feature files.

## Interaction

Ask for:

- decision made,
- alternatives considered,
- trade-offs accepted,
- reversibility and impact.

## Routing Rules

- Hard-to-reverse or architecture-shaping decision:
  - Create or update ADR draft in `docs/decisions/NNN-*.md`.
- Design-level change without full ADR threshold:
  - Update relevant file in `docs/design/`.
- Small implementation note:
  - Capture in plan notes or commit-message guidance.

## Output

- Decision capture summary
- File(s) created/updated
- Follow-up documentation tasks

## Principle

Documentation effort should be proportional to decision importance.
