# 001 - Export Safari Reading List

Status: IN PROGRESS
Owner: Maintainers
Last Updated: 2026-04-05

## User Story

As a user of this MCP server
I want to export Safari Reading List entries to a file
So that I can archive, analyze, or process my reading queue outside Safari

## Problem Statement

The project currently has no implemented Safari Reading List functionality. We need an initial, useful capability that proves end-to-end integration on macOS and provides stable output that downstream workflows can consume.

## Scope

In scope:

- Read Safari Reading List entries on macOS.
- Export all entries to a file.
- Export a filtered subset by time range when timestamp data is available.
- Default to a one-week range when no explicit range is provided.
- Return export summary metadata (entry count, output path, applied filters).

Out of scope:

- Mutating Reading List entries (add/remove/update).
- Cross-browser support.
- Rich de-duplication or conflict resolution.
- Cloud sync diagnostics.

## Use Cases

- Export entire reading list to JSON for backup.
- Export "entries from last 7 days" for weekly review.
- Export entries between explicit start/end datetimes for reporting windows.
- Run export from MCP client and receive both file location and summary.

## Functional Requirements

- The feature exposes an MCP interface for export.
- The interface supports two modes:
  - full export (explicitly requested),
  - range export (default mode; start/end inclusive).
- Output format is JSON only (structured and stable JSON v1 schema).
- If no range is provided, the effective range is the past 7 days ending at invocation time.
- Time input and output timestamps use RFC 3339 format.
- Each exported record includes, when available:
  - title,
  - URL,
  - added timestamp,
  - preview/notes metadata if accessible.
- If timestamp data is unavailable from Safari integration, the export must:
  - still succeed for full export,
  - clearly report why date-range filtering cannot be applied.

## Non-Functional Requirements

- macOS-only behavior is explicit.
- Errors are actionable (permission denied, Safari unavailable, script failure, invalid range).
- Exports are deterministic for identical source data and parameters.
- Implementation avoids destructive operations.

## Acceptance Criteria

- [ ] MCP client can request full reading list export and receive success response with output path and count.
- [ ] Export file is created and parseable JSON.
- [ ] MCP client can request range-limited export using RFC 3339 timestamps.
- [ ] If range is omitted, export defaults to last 7 days and reports the effective range used.
- [ ] Invalid range (`start > end`) returns validation error.
- [ ] If date filtering is requested but unsupported by available Safari metadata, response is explicit and non-ambiguous.
- [ ] At least one integration verification is documented for a real macOS Safari environment.

## Interface Draft (subject to refinement)

Tool name (draft): `export_reading_list`

Inputs:

- `output_path` (string, required)
- `start_time` (string RFC 3339, optional)
- `end_time` (string RFC 3339, optional)
- `full_export` (boolean, optional; default `false`)

Outputs:

- `success` (boolean)
- `output_path` (string)
- `exported_count` (integer)
- `total_count` (integer)
- `filters_applied` (object)
- `warnings` (array of strings)

## Examples

- Input:
  - `output_path`: `./exports/reading-list-week.json`
- Output:
  - `success`: `true`
  - `exported_count`: `12`
  - `total_count`: `143`
  - `filters_applied`: `{ "start_time": "2026-03-29T00:00:00Z", "end_time": "2026-04-05T00:00:00Z", "default_range": true }`

- Input:
  - `output_path`: `./exports/reading-list-all.json`
  - `full_export`: `true`
- Output:
  - `success`: `true`
  - `exported_count`: `143`
  - `total_count`: `143`

- Input:
  - `output_path`: `./exports/reading-list-custom-window.json`
  - `start_time`: `2026-03-29T00:00:00Z`
  - `end_time`: `2026-04-05T00:00:00Z`
- Output:
  - `success`: `true`
  - `exported_count`: `12`
  - `total_count`: `143`
  - `filters_applied`: `{ "start_time": "...", "end_time": "..." }`

## Verification

Manual steps:

- Prepare Safari with known Reading List entries.
- Run MCP server locally.
- Invoke full export and verify file creation + JSON structure.
- Invoke range export for last 7 days and verify subset size and timestamps.
- Invoke invalid range and verify validation error.
- Temporarily simulate missing permissions/automation access and verify actionable error.

Automated checks (initial target):

- Unit test parameter validation (`start_time`, `end_time`, `full_export` interactions).
- Unit test export serialization schema stability.
- Adapter-level tests with fixture data for full and range filtering behavior.
- Contract test for MCP tool response shape.

Execution notes (2026-04-05):

- Automated test suite implemented and passing (`15` pytest tests).
- Local macOS verification reached real Safari bookmarks access path but was blocked by OS permissions (`Permission denied` on `~/Library/Safari/Bookmarks.plist`).
- Error path now returns actionable guidance for Full Disk Access configuration.

## Risks and Open Questions

- Safari Reading List timestamp availability may be limited depending on integration method.
- AppleScript/automation access prompts may affect first-run behavior.
- The starter script in `~/git/gitjournal/Tools/safari-reading-list-export.py` reads Safari data from `~/Library/Safari/Bookmarks.plist`; we should validate this remains reliable across Safari/macOS versions before locking implementation details.
