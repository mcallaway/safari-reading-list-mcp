"""Persistent article state tracking via a local SQLite database.

States: pending -> added | skipped
- pending: seen by the pipeline, awaiting a decision
- added:   incorporated into Second Brain (terminal)
- skipped: reviewed and consciously excluded (terminal)
"""
from __future__ import annotations

import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal, TypedDict

SCHEMA_VERSION = 1
DEFAULT_DB_PATH = Path("~/.local/share/srl/state.db").expanduser()

# Max params per SQLite IN-clause query; avoids SQLITE_MAX_VARIABLE_NUMBER limit.
_CHUNK = 500

ArticleStatus = Literal["pending", "added", "skipped"]


class ArticleRecord(TypedDict):
    url: str
    status: str
    first_seen_at: str
    updated_at: str


def open_db(path: Path) -> sqlite3.Connection:
    """Open (or create) the state DB at path and return a connection."""
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    _ensure_schema(conn)
    return conn


def _ensure_schema(conn: sqlite3.Connection) -> None:
    version: int = conn.execute("PRAGMA user_version").fetchone()[0]
    if version == 0:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS articles (
                url           TEXT PRIMARY KEY,
                status        TEXT NOT NULL CHECK(status IN ('pending', 'added', 'skipped')),
                first_seen_at TEXT NOT NULL,
                updated_at    TEXT NOT NULL
            );
            PRAGMA user_version = 1;
            """
        )
    elif version != SCHEMA_VERSION:
        raise RuntimeError(
            f"Unsupported state DB schema version {version} "
            f"(expected {SCHEMA_VERSION}). "
            "Delete the DB file to reset, or migrate manually."
        )


def upsert_pending(conn: sqlite3.Connection, urls: list[str]) -> int:
    """Insert urls not already in the DB as 'pending'. Never downgrades existing state.

    Returns the count of newly inserted rows.
    """
    if not urls:
        return 0
    now = _now_iso()
    before: int = conn.execute("SELECT COUNT(*) FROM articles").fetchone()[0]
    conn.executemany(
        "INSERT OR IGNORE INTO articles (url, status, first_seen_at, updated_at) "
        "VALUES (?, 'pending', ?, ?)",
        [(url, now, now) for url in urls],
    )
    conn.commit()
    after: int = conn.execute("SELECT COUNT(*) FROM articles").fetchone()[0]
    return after - before


def filter_unprocessed(conn: sqlite3.Connection, urls: list[str]) -> list[str]:
    """Return urls not in a terminal state ('added' or 'skipped').

    Includes urls not yet in the DB (implicitly pending). Preserves input order.
    """
    if not urls:
        return []
    terminal: set[str] = set()
    for i in range(0, len(urls), _CHUNK):
        chunk = urls[i : i + _CHUNK]
        placeholders = ",".join("?" * len(chunk))
        rows = conn.execute(
            f"SELECT url FROM articles "
            f"WHERE url IN ({placeholders}) AND status IN ('added', 'skipped')",
            chunk,
        ).fetchall()
        terminal.update(str(row[0]) for row in rows)
    return [url for url in urls if url not in terminal]


def count_by_status(conn: sqlite3.Connection, urls: list[str], status: ArticleStatus) -> int:
    """Return how many of the given urls have the given status in the DB."""
    if not urls:
        return 0
    total = 0
    for i in range(0, len(urls), _CHUNK):
        chunk = urls[i : i + _CHUNK]
        placeholders = ",".join("?" * len(chunk))
        row = conn.execute(
            f"SELECT COUNT(*) FROM articles WHERE url IN ({placeholders}) AND status = ?",
            [*chunk, status],
        ).fetchone()
        total += int(row[0])
    return total


def mark_url(conn: sqlite3.Connection, url: str, status: Literal["added", "skipped"]) -> None:
    """Transition url to 'added' or 'skipped'. Raises ValueError if url is not in the DB."""
    now = _now_iso()
    result = conn.execute(
        "UPDATE articles SET status = ?, updated_at = ? WHERE url = ?",
        (status, now, url),
    )
    conn.commit()
    if result.rowcount == 0:
        raise ValueError(f"URL not found in state DB: {url!r}")


def get_by_status(conn: sqlite3.Connection, status: ArticleStatus) -> list[ArticleRecord]:
    """Return all articles with the given status, most recently seen first."""
    rows = conn.execute(
        "SELECT url, status, first_seen_at, updated_at FROM articles "
        "WHERE status = ? ORDER BY first_seen_at DESC",
        (status,),
    ).fetchall()
    return [
        ArticleRecord(
            url=str(row[0]),
            status=str(row[1]),
            first_seen_at=str(row[2]),
            updated_at=str(row[3]),
        )
        for row in rows
    ]


def get_stats(conn: sqlite3.Connection) -> dict[str, int]:
    """Return count of articles per status. Always includes all three states."""
    rows = conn.execute(
        "SELECT status, COUNT(*) FROM articles GROUP BY status"
    ).fetchall()
    counts: dict[str, int] = {"pending": 0, "added": 0, "skipped": 0}
    for row in rows:
        counts[str(row[0])] = int(row[1])
    return counts


def _now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()
