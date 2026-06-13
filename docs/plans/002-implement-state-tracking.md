# 002 - Implement Reading List State Tracking

Status: PROPOSED
Created: 2026-06-13
Updated: 2026-06-13
Related Feature: `docs/features/002-reading-list-state-tracking.md`

## Context

Feature 002 adds persistent state to the Reading List pipeline. Without it, every
export is a full snapshot with no memory of what has already been processed. With
1084 entries in the local Reading List and a growing backlog, a human or AI agent
needs to pick up where it left off across sessions.

The state model is simple: three states (`pending` -> `added` | `skipped`), stored
in a local SQLite database. State is written automatically on export and updated
manually or by an MCP agent after processing.

This plan delivers all new modules, CLI surface, MCP tools, and tests for Feature 002.

## Goals

- Implement a `state.py` module with SQLite-backed article state management.
- Integrate state tracking into all export commands (upsert on export, `--unprocessed-only` flag).
- Extend export log output with state-aware counts (`new_to_db`, `already_added`, `already_skipped`).
- Add `srl state` CLI group: `list`, `mark`, `stats`.
- Add MCP tools: `list_reading_list_state`, `mark_reading_list_item`.
- Make state DB path configurable via CLI flag and environment variable.
- Maintain full backward compatibility: existing export behavior unchanged when `--unprocessed-only` is not used.

## Non-goals

- Syncing state across machines.
- State tracking for non-Reading-List sources (Gmail, Notes).
- Bulk import of historical export files into state DB.
- Migrations beyond initial schema bootstrap (can be deferred to a later plan if needed).
- UI for browsing or editing state.

## Phases

- Phase 1 - State DB module
  - Create `safari_reading_list_mcp/state.py`.
  - SQLite schema: `articles(url TEXT PRIMARY KEY, status TEXT, first_seen_at TEXT, updated_at TEXT)`.
  - Schema versioned via SQLite `user_version` pragma (set to `1` on init).
  - `init_db(path)` -- create DB and table if not present; verify schema version.
  - `upsert_pending(conn, urls)` -- insert new URLs as `pending`; do not downgrade existing state.
  - `filter_pending(conn, urls)` -- return subset of URLs in `pending` state.
  - `mark_url(conn, url, status)` -- transition to `added` or `skipped`; raise if URL unknown.
  - `get_by_status(conn, status)` -- return all articles matching a state.
  - `get_stats(conn)` -- return count per state.
  - Default DB path: `~/.local/share/srl/state.db` (created with parent dirs if absent).
  - Unit tests for all transition logic, no-downgrade guarantee, and empty DB bootstrap.

- Phase 2 - Export integration
  - Update `service.py`: accept optional `state_db_path` and `unprocessed_only` parameters.
  - On any export run: call `upsert_pending` with all exported URLs.
  - When `unprocessed_only=True`: call `filter_pending` before writing output file.
  - Extend `ExportResult` with `new_to_db`, `already_added`, `already_skipped` counts.
  - Update `_log_export_result` in `cli.py` to log new counts.
  - Add `--unprocessed-only` and `--db-path` flags to `week`, `range`, and `all` subcommands.
  - Support `SRL_STATE_DB` environment variable as fallback for DB path.
  - Unit tests for filtering, upsert integration, and backward-compatible path (no state DB used when flag absent).

- Phase 3 - `srl state` CLI group
  - Add `srl state list [--status pending|added|skipped]` -- tabular output to stdout.
  - Add `srl state mark --url <url> --status added|skipped` -- explicit state transition.
  - Add `srl state stats` -- one line per state with count.
  - All `state` subcommands accept `--db-path` and respect `SRL_STATE_DB`.
  - Unit/integration tests for each subcommand.

- Phase 4 - MCP tools
  - Add `list_reading_list_state` tool to `server.py`:
    - Input: optional `status` filter (`pending`, `added`, `skipped`).
    - Output: list of `{url, status, first_seen_at, updated_at}` records.
  - Add `mark_reading_list_item` tool to `server.py`:
    - Input: `url`, `status` (`added` or `skipped`).
    - Output: success/error response.
  - Both tools use the configured DB path (env var or default).
  - Tests for tool response shapes.

- Phase 5 - Verification and docs sync
  - Run full test suite and confirm baseline holds.
  - Execute manual verification checklist from Feature 002.
  - Update Feature 002 acceptance criteria checkboxes.
  - Update `docs/plans/README.md` status.

## Deliverables

- `safari_reading_list_mcp/state.py` -- new module (state DB logic)
- `safari_reading_list_mcp/service.py` -- updated (state integration, new result fields)
- `safari_reading_list_mcp/cli.py` -- updated (new flags, `srl state` group)
- `safari_reading_list_mcp/server.py` -- updated (two new MCP tools)
- `tests/test_state.py` -- new test file
- Updated tests for `service.py` and `cli.py`

## Outcomes

- A user can run `srl export all --unprocessed-only` and receive only articles not yet
  `added` or `skipped`, regardless of how many times the export has run before.
- An AI agent can query pending articles via MCP and mark them `added` or `skipped`
  after processing, enabling incremental second-brain ingestion.
- The state DB is human-readable, easy to back up, and queryable with any SQLite tool.

## Risks and Unknowns

- URL canonicalization: URLs read from `Bookmarks.plist` may vary slightly across
  Safari versions (trailing slashes, query params). If the same article has two
  slightly different URL forms, it will appear as two DB entries. Worth monitoring
  on first real run against the 1084-entry dataset.
- First export with state enabled inserts all 1084 existing entries as `pending`.
  This is correct but worth calling out so it is not surprising.
- `user_version` pragma is a lightweight versioning approach. If schema changes
  are needed in a future plan, a migration strategy will need to be defined then.

## Verification

- Unit tests:
  - State transition rules (no downgrade from `added`/`skipped` to `pending`).
  - `filter_pending` returns correct subset.
  - `get_stats` returns accurate counts.
  - `mark_url` raises on unknown URL.
  - DB bootstraps correctly from empty path.
- Integration/manual checks:
  - Fresh run: confirm DB created and all exported URLs inserted as `pending`.
  - Second run with `--unprocessed-only`: confirm only `pending` items returned.
  - `srl state mark` + re-export: confirm marked items excluded.
  - `srl state stats`: confirm counts match expectations.
  - MCP agent: confirm `list_reading_list_state` and `mark_reading_list_item` respond correctly.
