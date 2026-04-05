# 001 - Implement Reading List Export

Status: IN PROGRESS
Created: 2026-04-05
Updated: 2026-04-05
Related Feature: `docs/features/001-export-safari-reading-list.md`

## Context

Feature 001 defines the first end-to-end capability for this repository: exporting Safari Reading List entries through an MCP interface to a JSON file. This work establishes the core server/tool structure, Safari data access adapter, and validation/error contract that future features will build on.

The project currently contains only a scaffold (`main.py`) and documentation workflows.

## Goals

- Implement a minimal but production-shaped MCP server entrypoint in Python.
- Add an MCP tool for reading list export that supports:
  - default last-7-days range export,
  - explicit range export (`start_time`, `end_time`),
  - explicit full export (`full_export=true`).
- Produce deterministic JSON export output with clear response metadata.
- Handle macOS/Safari integration errors with actionable messages.
- Document verification steps and execute initial validation.

## Non-goals

- Adding entries to Reading List.
- Removing or updating entries.
- Multi-format export (JSON-only for v1).
- Non-macOS support.

## Deliverables

- Runtime implementation in repository code for MCP tool registration and execution.
- Safari adapter module that reads Reading List source data and normalizes item records.
- JSON export writer and response schema handling.
- Basic automated tests for parsing/filtering/validation and response shape.
- Updated documentation where implementation details become concrete.

## Phases

- Phase 1 - Server and interface skeleton
  - Define module layout and tool function signatures.
  - Wire MCP server startup and tool registration.
- Phase 2 - Safari data extraction adapter
  - Implement Reading List extraction from Safari source data.
  - Normalize title/url/date/preview fields.
- Phase 3 - Filtering and export output
  - Implement default week range behavior.
  - Implement explicit range and full export branching.
  - Write JSON output and return metadata.
- Phase 4 - Validation and error handling
  - RFC 3339 parsing/validation.
  - Invalid range and unsupported timestamp-path handling.
  - macOS/Safari availability and permission error messages.
- Phase 5 - Verification and documentation sync
  - Add and run tests.
  - Execute manual verification checklist on macOS.
  - Update docs/plans status and related references.

## Outcomes

- A user can invoke one MCP tool to export Safari Reading List entries to JSON.
- The tool has stable behavior for default-range, custom-range, and full-export modes.
- The repository transitions from scaffold-only to first concrete MCP capability.

## Risks and Unknowns

- Reliability of Safari Reading List timestamp fields across macOS/Safari versions.
- First-run automation permissions may cause user-environment variability.
- Reading List source structure may differ from assumptions in starter script inspiration.

## Verification

- Unit tests:
  - time input parsing and range validation,
  - default-week range calculation,
  - filtering behavior with fixture timestamps,
  - JSON payload schema expectations.
- Integration/manual checks:
  - full export on local macOS Safari dataset,
  - default-range export,
  - custom-range export,
  - invalid-input and permission-failure paths.

## Dependencies

- Python environment and `mcp` dependency already available.
- Local Safari profile with Reading List entries for manual verification.

## Exit Criteria

- Feature 001 acceptance criteria are met and demonstrable.
- Plan status can be moved from `PROPOSED` to `IN PROGRESS` at implementation start, then to `COMPLETE` when verification and docs sync are done.

## Progress Notes (2026-04-05)

- Phase 1 complete: MCP server skeleton and `export_reading_list` tool implemented.
- Phase 2 complete: Safari bookmarks plist adapter implemented with Reading List extraction.
- Phase 3 complete: JSON export and filtering modes implemented (default week, explicit range, full export).
- Phase 4 complete: validation and actionable error handling implemented, including permission guidance.
- Phase 5 partially complete: automated tests and docs sync completed.

## Remaining Work

- Execute successful manual export on real Safari dataset after granting Full Disk Access to terminal/MCP host.
- If manual verification succeeds, move plan status to `COMPLETE` and close plan.
