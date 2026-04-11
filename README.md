# safari-reading-list-mcp

An Anthropic MCP server project for Apple Safari Reading List workflows on macOS.

This repository now provides a working MCP server and CLI for exporting Safari Reading List data to JSON.

## Project Status

- Feature 001 is complete: export Safari Reading List entries (all, default week, custom range).
- MCP server entrypoint is active via `main.py` and `safari_reading_list_mcp/server.py`.
- CLI entrypoint `srl` is available with export and serve commands.
- Quality checks are automated with mise tasks for lint, type checks, and tests.

## Goals

- Expose MCP tools/resources to read and export Safari Reading List items.
- Support adding new items to Safari Reading List.
- Keep implementation and decisions documented for durable project memory.

## Requirements

- macOS (Safari Reading List target platform)
- Python 3.14
- `uv`
- Optional: `mise` for tool version management

## Quick Start

1. Install dependencies:
   - `uv sync`
2. Run MCP server (stdio transport):
   - `uv run python main.py`
3. Use CLI:
   - `srl --help`
4. Run all checks:
   - `mise run test:all`

## Repository Layout

- `main.py` - runtime entrypoint that starts the MCP server
- `safari_reading_list_mcp/` - implementation modules (server, service, adapter, time/filter/export helpers, CLI)
- `pyproject.toml` - project metadata and dependencies
- `mise.toml` - local tool/runtime configuration
- `.mise/tasks/` - reusable project tasks (lint, types, unit, coverage)
- `AGENTS.md` - primary agent/human collaboration conventions
- `docs/` - project memory (plans, features, design, decisions, guides)
- `.github/prompts/` - reusable workflow prompts for agent sessions

## Development Workflow

Use the documentation cycle:

- define behavior in `docs/features/`
- create execution plans in `docs/plans/`
- capture hard-to-reverse decisions in `docs/decisions/`
- maintain architecture rationale in `docs/design/`
- keep practical usage notes in `docs/guides/`

For agent/human operating conventions, start with `AGENTS.md`.
