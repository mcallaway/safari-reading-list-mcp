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

- No active plan. Feature 002 complete.

## Next Steps

- Define Feature 003 or next pipeline integration as priorities emerge.
- Consider ADR for long-term Safari integration strategy (plist-only vs multi-adapter).
- See `tmp/pipeline-vision.md` for broader knowledge ingestion pipeline ideas.

## Recent Work

- Feature 002 complete: Reading List state tracking.
  - SQLite state DB (`pending` -> `added` | `skipped`)
  - `--unprocessed-only` flag on all export commands
  - `srl state` CLI group: stats, list, mark
  - MCP tools: `list_reading_list_state`, `mark_reading_list_item`
  - 66 tests passing, pyright and ruff clean
  - Verified against 1084-entry local Safari Reading List

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
