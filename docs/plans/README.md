# Plans

## Purpose

Plans are the project's GPS indicator for active and upcoming work. When complete, plans become historical records of what was delivered and why.

## What This File Contains

- Current Focus
- Next Steps
- Recent Work
- Key References

## Plan File Format

- Numbered title, e.g. `001-build-mcp-server-scaffold.md`
- Status header: `PROPOSED`, `IN PROGRESS`, or `COMPLETE`
- Dates (created/updated/completed)

## Standards

- Include clear goals and expected outcomes.
- Prefer bullet lists to dense prose.
- Keep scope and non-goals explicit.

## Current Focus

- Define next feature set (for example, add Reading List items via MCP).
- Decide whether Safari integration should expand beyond plist reading in the next increment.

## Next Steps

- Create Feature 002 proposal for writing/adding Reading List entries.
- Create Plan 002 with phased implementation for add-item workflow.
- Evaluate ADR need for long-term Safari integration strategy (plist-only vs multi-adapter).

## Recent Work

- Repository scaffold initialized with Python 3.14, uv, and `mcp` dependency.
- Agentic development structure established (`AGENTS.md`, docs scheme, prompt library).
- Feature spec created: `docs/features/001-export-safari-reading-list.md`.
- Plan created: `docs/plans/001-implement-reading-list-export.md`.
- Plan 001 started (`IN PROGRESS`).
- Core implementation shipped with pytest coverage (`15` tests passing).
- Design note added: `docs/design/001-reading-list-export-architecture.md`.
- Plan 001 completed with successful real local Safari export verification.

## Key References

- `docs/features/README.md`
- `docs/design/README.md`
- `docs/decisions/README.md`
- `AGENTS.md`
