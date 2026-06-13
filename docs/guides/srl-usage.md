# srl Usage Guide

## Quick Reference

```
# Export
srl export week --output out.json                    # last 7 days
srl export all  --output out.json                    # full reading list
srl export range --start 2026-05-01T00:00:00Z \
                 --end   2026-05-31T23:59:59Z \
                 --output out.json                   # explicit range

# Export only unprocessed (pending) articles
srl export week --unprocessed-only --output out.json
srl export all  --unprocessed-only --output out.json

# State
srl state stats                                      # count per status
srl state list                                       # list pending articles
srl state list --status added                        # list added articles
srl state mark --url <url> --status added            # mark as incorporated
srl state mark --url <url> --status skipped          # mark as skipped

# Verbose output
srl --log-level INFO export all --output out.json

# MCP server
srl serve
```

---

## Concepts

### Article states

Every article you have ever exported enters a lifecycle:

| State | Meaning | Set by |
|-------|---------|--------|
| `pending` | Seen by the pipeline; awaiting a decision | Automatic on first export |
| `added` | Incorporated into Second Brain | Human or AI agent |
| `skipped` | Reviewed and consciously excluded | Human or AI agent |

`added` and `skipped` are terminal: re-exporting the same URL never resets the state.

### State database

The state DB lives at `~/.local/share/srl/state.db` by default. It is a plain SQLite file — inspectable with any SQLite tool and straightforward to back up or delete.

Override via:
- `--db-path /path/to/state.db` on any command
- `SRL_STATE_DB=/path/to/state.db` environment variable

---

## Use Cases

### 1. First-run export

Export everything and register all articles as `pending` in the state DB.

```sh
srl --log-level INFO export all --output ./exports/all.json
```

Sample output (INFO level):
```
INFO safari_reading_list_mcp.cli: success=True
INFO safari_reading_list_mcp.cli: output_path=exports/all.json
INFO safari_reading_list_mcp.cli: exported_count=1084
INFO safari_reading_list_mcp.cli: total_count=1084
INFO safari_reading_list_mcp.cli: new_to_db=1084
INFO safari_reading_list_mcp.cli: already_added=0
INFO safari_reading_list_mcp.cli: already_skipped=0
```

All 1084 articles are now `pending` in the state DB.

---

### 2. Incremental export (working through a backlog)

Once articles are in the DB, use `--unprocessed-only` to get only those still
awaiting a decision:

```sh
srl export all --unprocessed-only --output ./exports/batch.json
```

On the first run, this returns all `pending` articles. After you mark some `added`
or `skipped`, subsequent runs return only what remains.

---

### 3. This week's new articles

Export only reading list entries added in the past 7 days. Combined with
`--unprocessed-only`, this gives you only newly-seen articles not yet processed:

```sh
srl export week --unprocessed-only --output ./exports/week.json
```

If you run this Monday through Friday, each run returns that week's additions
you haven't yet acted on.

---

### 4. Custom date range

Export a specific calendar month:

```sh
srl export range \
  --start 2026-05-01T00:00:00Z \
  --end   2026-05-31T23:59:59Z \
  --output ./exports/may.json
```

All times are inclusive. Use RFC 3339 format with a `Z` suffix for UTC.

---

### 5. Check what's left to process

Before starting a work session, see where you stand:

```sh
srl state stats
```

Output:
```
pending    312
added       54
skipped    718
```

---

### 6. Browse pending articles

List all articles still waiting for a decision:

```sh
srl state list
```

Output (tab-separated: status, url, first_seen_at):
```
pending	https://example.com/article-a	2026-05-04T12:00:00+00:00
pending	https://example.com/article-b	2026-05-04T12:00:01+00:00
```

Filter by a specific state:

```sh
srl state list --status added
srl state list --status skipped
```

---

### 7. Mark articles after reviewing them

After adding an article's content to Second Brain:

```sh
srl state mark --url https://example.com/article-a --status added
```

After deciding an article isn't worth keeping:

```sh
srl state mark --url https://example.com/article-b --status skipped
```

Confirmation is printed to stdout:

```
Marked 'https://example.com/article-a' as added.
```

The article no longer appears in `--unprocessed-only` exports.

---

### 8. AI agent workflow (MCP)

Run the MCP server for use with an AI assistant:

```sh
srl serve
```

The server exposes three tools:

| Tool | Description |
|------|-------------|
| `export_reading_list` | Export entries to JSON (same modes as CLI) |
| `list_reading_list_state` | List articles by state (default: `pending`) |
| `mark_reading_list_item` | Transition a URL to `added` or `skipped` |

A typical agent session:
1. Agent calls `list_reading_list_state` to get pending articles.
2. Agent summarises each article and decides to incorporate or skip.
3. Agent calls `mark_reading_list_item` for each decision.
4. Human reviews the Second Brain additions and confirms.

---

### 9. Verbose logging

All informational output goes to stderr, keeping stdout clean for JSON piping.

```sh
srl --log-level INFO export week --output out.json
srl --log-level DEBUG export week --output out.json   # full diagnostic trace
```

Pipe JSON to another tool while still seeing logs:

```sh
srl --log-level INFO export all --output /dev/stdout 2>srl.log | jq '.[] | .url'
```

---

### 10. Override the bookmarks source

For testing against a different plist (e.g. a copy from another machine):

```sh
srl export all --bookmarks-path ~/Desktop/Bookmarks.plist --output out.json
```

---

## Configuration Reference

| Setting | CLI flag | Environment variable | Default |
|---------|----------|---------------------|---------|
| State DB path | `--db-path` | `SRL_STATE_DB` | `~/.local/share/srl/state.db` |
| Bookmarks path | `--bookmarks-path` | — | `~/Library/Safari/Bookmarks.plist` |
| Log level | `--log-level` | — | `WARNING` |

---

## Troubleshooting

**`PermissionError` on export**

Safari's bookmarks file requires Full Disk Access. Go to:
System Settings → Privacy & Security → Full Disk Access → enable Terminal (or your MCP host).

**`srl state mark` exits non-zero**

The URL is not in the state DB. Export first to register it as `pending`:

```sh
srl export all --output /dev/null
srl state mark --url <url> --status added
```

**State DB in unexpected location**

Check the `SRL_STATE_DB` environment variable; it overrides `--db-path` defaults.
Inspect with any SQLite browser or:

```sh
sqlite3 ~/.local/share/srl/state.db "SELECT status, COUNT(*) FROM articles GROUP BY status"
```
