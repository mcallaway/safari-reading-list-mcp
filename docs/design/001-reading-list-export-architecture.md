# 001 - Reading List Export Architecture

Status: IMPLEMENTED
Last Updated: 2026-06-13
Related Feature: `docs/features/001-export-safari-reading-list.md`
Related Plan: `docs/plans/001-implement-reading-list-export.md`

## Overview

The implementation uses a small, composable package rooted at `safari_reading_list_mcp/`.

Core flow:

1. MCP tool or CLI entrypoint receives request fields.
2. Service layer resolves effective filter mode (default week, explicit range, or full export).
3. Safari adapter reads Reading List entries from Safari bookmarks plist.
4. Export layer applies filtering and writes JSON payload.
5. State layer upserts exported URLs into the local SQLite state DB (if configured).
6. Response metadata is returned to caller.

## Module Responsibilities

- `safari_reading_list_mcp/server.py`
  - Defines `FastMCP` server and registers MCP tools.
  - Converts runtime exceptions into structured failure payloads.
- `safari_reading_list_mcp/service.py`
  - Orchestrates read/filter/export/state behavior.
  - Enforces mode semantics and response shape.
- `safari_reading_list_mcp/state.py`
  - SQLite-backed article state DB (`pending` → `added` | `skipped`).
  - All state transitions and queries go through this module.
  - Default DB path: `~/.local/share/srl/state.db`.
  - Schema versioned via SQLite `user_version` pragma (v1).
- `safari_reading_list_mcp/safari_bookmarks.py`
  - Reads and traverses Safari bookmarks plist.
  - Extracts normalized reading list entries.
- `safari_reading_list_mcp/time_utils.py`
  - Parses RFC 3339 values.
  - Resolves default last-7-days behavior.
- `safari_reading_list_mcp/exporter.py`
  - Applies inclusive date-range filters.
  - Writes deterministic JSON output.
- `safari_reading_list_mcp/models.py`
  - Defines `ReadingListItem` data structure.

## Error Handling

- Missing bookmarks file: explicit `FileNotFoundError`.
- Permission denied on bookmarks file: actionable `PermissionError` with Full Disk Access guidance.
- Missing Reading List container: explicit `ValueError`.
- Invalid date range: explicit `ValueError` (`start_time <= end_time`).
- Unfilterable date-range request (no parseable timestamps): explicit `ValueError`.
- `mark_url` on unknown URL: explicit `ValueError`.
- Unsupported state DB schema version: explicit `RuntimeError` with guidance to delete or migrate.

## Verification Coverage

- Unit tests verify:
  - RFC 3339 parsing and default-week range behavior,
  - range filtering and JSON serialization,
  - plist extraction behavior,
  - service-level mode behavior,
  - MCP tool success and failure response shape,
  - state DB transitions, no-downgrade guarantee, and upsert behavior.
- Feature coverage tracked via `features/state-tracking.feature.yaml` (28/28 requirements).

## Known Limitations

- Manual end-to-end export against local Safari may require granting Full Disk Access to Terminal or MCP host process.
- Current implementation uses Bookmarks.plist data source only; no AppleScript fallback yet.
- URL canonicalization is deferred: tracking URLs (e.g. newsletter redirects) appear as separate DB entries from their canonical targets. See `tmp/feature-request-url-canonicalization.md`.
