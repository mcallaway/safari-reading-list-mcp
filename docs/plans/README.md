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

- Execute Plan 001 for Feature 001: Safari Reading List JSON export via MCP.
- Implement first usable MCP server skeleton in Python with `export_reading_list` tool.
- Validate Safari Reading List source handling and timestamp filtering behavior on macOS.

## Next Steps

- Move `docs/plans/001-implement-reading-list-export.md` to `IN PROGRESS` and begin Phase 1 implementation.
- Decide and document concrete Safari integration approach (Bookmarks.plist adapter now, AppleScript fallback/alternative later).
- Draft a design note for MCP server/module layout once implementation structure is finalized.

## Recent Work

- Repository scaffold initialized with Python 3.14, uv, and `mcp` dependency.
- Agentic development structure established (`AGENTS.md`, docs scheme, prompt library).
- Feature spec created: `docs/features/001-export-safari-reading-list.md`.
- Plan created: `docs/plans/001-implement-reading-list-export.md`.

## Key References

- `docs/features/README.md`
- `docs/design/README.md`
- `docs/decisions/README.md`
- `AGENTS.md`
