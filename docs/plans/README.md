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

- Plan 002 active: implement reading list state tracking (SQLite, `pending`/`added`/`skipped`, `--unprocessed-only`, MCP tools).

## Next Steps

- Begin Plan 002, Phase 1: implement `safari_reading_list_mcp/state.py`.
- Evaluate ADR need for state DB schema versioning approach.
- Consider ADR for long-term Safari integration strategy (plist-only vs multi-adapter).

## Recent Work

- Feature 002 defined: Reading List state tracking (`pending` -> `added` | `skipped`).
- Plan 002 written and ready for implementation.

## Recent Work

- Feature 001 completed: Safari Reading List export (full, default week, custom range).
- Plan 001 completed and verified against real local Safari data.
- CLI shipped with `srl export` and `srl serve` commands.
- Logging behavior aligned for pipelines (human-readable logs to stderr, JSON output clean on stdout).
- Typing baseline strengthened with pyright-compatible annotations and TypedDict response shapes.
- Mise task set added and normalized (`test:lint`, `test:types`, `test:unit`, `test:coverage`, `test:all`).
- Current automated baseline: 21 pytest tests passing with lint and type checks passing.

## Key References

- `docs/features/README.md`
- `docs/design/README.md`
- `docs/decisions/README.md`
- `AGENTS.md`
