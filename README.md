# safari-reading-list-mcp

An Anthropic MCP server project for Apple Safari Reading List workflows on macOS.

This repository is currently in scaffold stage: Python runtime and MCP dependency are in place, with a documentation-first, agentic development workflow now established.

## Project Status

- Runtime scaffold exists (`main.py`).
- MCP integration and Safari Reading List functionality are planned.
- Documentation, planning, and prompt workflows are established under `docs/` and `.github/prompts/`.

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
2. Run current entrypoint:
   - `uv run python main.py`

## Repository Layout

- `main.py` - runtime entrypoint (currently placeholder behavior)
- `pyproject.toml` - project metadata and dependencies
- `mise.toml` - local tool/runtime configuration
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
