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

- Define Safari Reading List feature scope and MCP tool contracts.
- Implement first usable MCP server skeleton in Python.
- Document architecture and platform constraints for macOS Safari integration.

## Next Steps

- Create first feature spec in `docs/features/` for reading list read/export/add operations.
- Create first implementation plan file (`001-...`) and begin execution.
- Decide and document Safari integration approach (`osascript` wrapper vs other mechanisms).

## Recent Work

- Repository scaffold initialized with Python 3.14, uv, and `mcp` dependency.
- Agentic development structure established (`AGENTS.md`, docs scheme, prompt library).

## Key References

- `docs/features/README.md`
- `docs/design/README.md`
- `docs/decisions/README.md`
- `AGENTS.md`
