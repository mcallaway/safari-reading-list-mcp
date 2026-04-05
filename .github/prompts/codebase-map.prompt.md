# Codebase Map

Create or refresh `docs/design/codebase-map.md` so architecture context stays current.

## Inputs

- Optional scope or refresh intent from caller: `$ARGUMENTS`

## Process

- Read current repository structure.
- Read existing `docs/design/codebase-map.md` if present.
- Read `AGENTS.md`, `docs/design/README.md`, and active plan(s).
- Map user/developer workflows to concrete files and directories.

## Required Output

Write or update `docs/design/codebase-map.md` with:

- Directory overview table
- File tables by area (runtime, config, docs, prompts)
- Workflow-to-file map
- Configuration reference (`pyproject.toml`, `mise.toml`, `.python-version`, `uv.lock`)
- Notes on stale/missing/inaccurate mappings when refreshing

## Repository-Specific Areas to Cover

- Runtime entrypoint: `main.py`
- Packaging/config: `pyproject.toml`, `mise.toml`
- Agent workflow assets: `AGENTS.md`, `.github/prompts/`
- Project memory: `docs/`
