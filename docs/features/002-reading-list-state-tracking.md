# 002 - Reading List State Tracking

Status: COMPLETE
Owner: Maintainers
Last Updated: 2026-06-13

## User Story

As a user of this MCP server
I want the tool to remember which Reading List entries have been processed
So that repeated exports only surface unprocessed items and I can track what has made it into Second Brain

## Problem Statement

The current export-only design has no memory. Every export returns the full dataset
(or a date-filtered subset), with no way to distinguish items that have already been
processed from new ones. As the Reading List backlog grows, this makes it impossible
to pick up where you left off or hand the agent only genuinely new work.

## Scope

In scope:

- A local SQLite database that persists article state across sessions.
- Three article states: `pending`, `added`, `skipped`.
- Automatic state set to `pending` on first export.
- CLI commands to query and manually update state.
- An `--unprocessed-only` flag on export commands that filters to `pending` items only.
- MCP tool equivalents so an AI agent can read and update state.

Out of scope:

- Syncing state across machines.
- State for non-Reading-List sources (Gmail, Notes).
- Bulk import of historical export files into state DB.
- UI for browsing state.

## Article States

| State | Set by | Meaning |
| --- | --- | --- |
| `pending` | automatic, on first export | URL has been seen by the pipeline; awaiting a decision |
| `added` | human or agent | Article has been incorporated into Second Brain |
| `skipped` | human or agent | Article was reviewed and consciously excluded |

Terminal states are `added` and `skipped`. An article in either state does not appear
in `--unprocessed-only` export results.

## Use Cases

- Run `srl export week --unprocessed-only` to get only pending items since last run.
- Run `srl export all --unprocessed-only` to work through the full backlog incrementally.
- Mark an article `added` after an AI agent writes a Second Brain note for it.
- Mark an article `skipped` when the agent or human decides it is not worth keeping.
- Query pending articles to see what still needs processing.

## Functional Requirements

- State DB lives at a configurable path, defaulting to `~/.local/share/srl/state.db`.
- On any export run, each exported URL is upserted into the DB:
  - If not present: inserted as `pending`.
  - If already `pending`: no change.
  - If already `added` or `skipped`: state is not downgraded.
- `--unprocessed-only` flag on all export subcommands: filters output to URLs in `pending` state only.
- Export log output (at INFO level) is extended with state-aware counts:
  - `new_to_db` -- URLs seen for the first time in this run (inserted as `pending`).
  - `already_added` -- URLs excluded because state is `added`.
  - `already_skipped` -- URLs excluded because state is `skipped`.
- New CLI surface: `srl state` group with:
  - `srl state list [--status pending|added|skipped]` -- query articles by state.
  - `srl state mark --url <url> --status added|skipped` -- manually transition an article.
  - `srl state stats` -- count of articles per state.
- MCP tools:
  - `list_reading_list_state` -- returns articles filtered by state.
  - `mark_reading_list_item` -- transitions a URL to `added` or `skipped`.

## Non-Functional Requirements

- State DB writes are atomic (SQLite transactions).
- Schema is versioned to allow future migrations.
- DB path is documented and easy to back up or delete.
- State operations do not require network access.

## Acceptance Criteria

- [x] Export log output includes `new_to_db`, `already_added`, and `already_skipped` counts.
- [x] Running `srl export week` for the first time populates the state DB with URLs in `pending` state.
- [x] Running `srl export week --unprocessed-only` a second time returns only `pending` URLs.
- [x] `srl state list --status pending` shows articles awaiting processing.
- [x] `srl state mark --url <url> --status added` transitions the article; it no longer appears in `--unprocessed-only` exports.
- [x] `srl state mark --url <url> --status skipped` behaves equivalently.
- [x] `srl state stats` shows accurate counts per state.
- [x] MCP agent can call `list_reading_list_state` and `mark_reading_list_item` successfully.
- [x] State DB path is configurable via CLI flag or environment variable.
- [x] Existing export behavior (without `--unprocessed-only`) is unchanged.

## Examples

First run:

```
srl --log-level INFO export week --unprocessed-only --output ./tmp/batch1.json
# INFO: exported_count=12, new_to_db=12
```

Second run (same week, 3 new items added):

```
srl --log-level INFO export week --unprocessed-only --output ./tmp/batch2.json
# INFO: exported_count=3, new_to_db=3
```

Mark items after agent processes them:

```
srl state mark --url https://example.com/article --status added
srl state mark --url https://example.com/boring --status skipped
```

Query pending work:

```
srl state list --status pending
# returns all URLs not yet added or skipped
```

Stats:

```
srl state stats
# pending: 9, added: 2, skipped: 1
```

## Verification

Manual steps:

- Fresh install: confirm DB is created on first export.
- Confirm `--unprocessed-only` excludes `added` and `skipped` articles.
- Confirm repeated export of same URL does not downgrade state.
- Confirm MCP agent can read and update state.

Automated checks:

- Unit tests for state transition logic (no downgrades, upsert behavior).
- Unit tests for `--unprocessed-only` filtering.
- Tests for `srl state mark` invalid transitions (e.g. `pending` -> `pending`).
- Schema migration test (empty DB bootstraps correctly).
