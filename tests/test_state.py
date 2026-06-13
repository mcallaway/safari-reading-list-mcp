from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from safari_reading_list_mcp import state


def make_db(tmp_path: Path) -> sqlite3.Connection:
    return state.open_db(tmp_path / "state.db")


class TestOpenDb:
    def test_creates_db_file(self, tmp_path: Path) -> None:
        db_path = tmp_path / "state.db"
        assert not db_path.exists()
        conn = state.open_db(db_path)
        conn.close()
        assert db_path.exists()

    def test_creates_parent_dirs(self, tmp_path: Path) -> None:
        db_path = tmp_path / "nested" / "dirs" / "state.db"
        conn = state.open_db(db_path)
        conn.close()
        assert db_path.exists()

    def test_bootstraps_schema_version(self, tmp_path: Path) -> None:
        conn = make_db(tmp_path)
        version: int = conn.execute("PRAGMA user_version").fetchone()[0]
        conn.close()
        assert version == state.SCHEMA_VERSION

    def test_idempotent_on_existing_db(self, tmp_path: Path) -> None:
        db_path = tmp_path / "state.db"
        state.open_db(db_path).close()
        conn = state.open_db(db_path)  # must not raise
        conn.close()

    def test_raises_on_unsupported_schema_version(self, tmp_path: Path) -> None:
        db_path = tmp_path / "state.db"
        raw = sqlite3.connect(str(db_path))
        raw.execute("PRAGMA user_version = 99")
        raw.commit()
        raw.close()
        with pytest.raises(RuntimeError, match="Unsupported state DB schema version"):
            state.open_db(db_path)


class TestUpsertPending:
    def test_inserts_new_urls_as_pending(self, tmp_path: Path) -> None:
        conn = make_db(tmp_path)
        count = state.upsert_pending(conn, ["https://a.com", "https://b.com"])
        assert count == 2
        rows = conn.execute("SELECT url, status FROM articles ORDER BY url").fetchall()
        assert [(r[0], r[1]) for r in rows] == [
            ("https://a.com", "pending"),
            ("https://b.com", "pending"),
        ]

    def test_returns_count_of_new_rows_only(self, tmp_path: Path) -> None:
        conn = make_db(tmp_path)
        state.upsert_pending(conn, ["https://a.com"])
        count = state.upsert_pending(conn, ["https://a.com", "https://b.com"])
        assert count == 1  # only b.com is new

    def test_returns_zero_for_empty_list(self, tmp_path: Path) -> None:
        conn = make_db(tmp_path)
        assert state.upsert_pending(conn, []) == 0

    def test_does_not_downgrade_added(self, tmp_path: Path) -> None:
        conn = make_db(tmp_path)
        state.upsert_pending(conn, ["https://x.com"])
        state.mark_url(conn, "https://x.com", "added")
        state.upsert_pending(conn, ["https://x.com"])
        row = conn.execute("SELECT status FROM articles WHERE url = ?", ("https://x.com",)).fetchone()
        assert row[0] == "added"

    def test_does_not_downgrade_skipped(self, tmp_path: Path) -> None:
        conn = make_db(tmp_path)
        state.upsert_pending(conn, ["https://x.com"])
        state.mark_url(conn, "https://x.com", "skipped")
        count = state.upsert_pending(conn, ["https://x.com"])
        assert count == 0
        row = conn.execute("SELECT status FROM articles WHERE url = ?", ("https://x.com",)).fetchone()
        assert row[0] == "skipped"

    def test_is_idempotent_for_pending(self, tmp_path: Path) -> None:
        conn = make_db(tmp_path)
        state.upsert_pending(conn, ["https://x.com"])
        count = state.upsert_pending(conn, ["https://x.com"])
        assert count == 0


class TestFilterUnprocessed:
    def test_excludes_added(self, tmp_path: Path) -> None:
        conn = make_db(tmp_path)
        state.upsert_pending(conn, ["https://a.com", "https://b.com"])
        state.mark_url(conn, "https://a.com", "added")
        assert state.filter_unprocessed(conn, ["https://a.com", "https://b.com"]) == ["https://b.com"]

    def test_excludes_skipped(self, tmp_path: Path) -> None:
        conn = make_db(tmp_path)
        state.upsert_pending(conn, ["https://a.com"])
        state.mark_url(conn, "https://a.com", "skipped")
        assert state.filter_unprocessed(conn, ["https://a.com"]) == []

    def test_includes_pending(self, tmp_path: Path) -> None:
        conn = make_db(tmp_path)
        state.upsert_pending(conn, ["https://a.com"])
        assert state.filter_unprocessed(conn, ["https://a.com"]) == ["https://a.com"]

    def test_includes_urls_not_in_db(self, tmp_path: Path) -> None:
        conn = make_db(tmp_path)
        assert state.filter_unprocessed(conn, ["https://unseen.com"]) == ["https://unseen.com"]

    def test_preserves_input_order(self, tmp_path: Path) -> None:
        conn = make_db(tmp_path)
        urls = ["https://c.com", "https://a.com", "https://b.com"]
        assert state.filter_unprocessed(conn, urls) == urls

    def test_returns_empty_for_empty_input(self, tmp_path: Path) -> None:
        conn = make_db(tmp_path)
        assert state.filter_unprocessed(conn, []) == []


class TestCountByStatus:
    def test_counts_pending_among_given_urls(self, tmp_path: Path) -> None:
        conn = make_db(tmp_path)
        state.upsert_pending(conn, ["https://a.com", "https://b.com", "https://c.com"])
        state.mark_url(conn, "https://a.com", "added")
        urls = ["https://a.com", "https://b.com", "https://c.com"]
        assert state.count_by_status(conn, urls, "pending") == 2

    def test_counts_added_among_given_urls(self, tmp_path: Path) -> None:
        conn = make_db(tmp_path)
        state.upsert_pending(conn, ["https://a.com", "https://b.com"])
        state.mark_url(conn, "https://a.com", "added")
        assert state.count_by_status(conn, ["https://a.com", "https://b.com"], "added") == 1

    def test_returns_zero_for_empty_list(self, tmp_path: Path) -> None:
        conn = make_db(tmp_path)
        assert state.count_by_status(conn, [], "pending") == 0

    def test_only_counts_within_given_urls(self, tmp_path: Path) -> None:
        conn = make_db(tmp_path)
        state.upsert_pending(conn, ["https://a.com", "https://b.com"])
        # Only ask about a.com; b.com should not be counted
        assert state.count_by_status(conn, ["https://a.com"], "pending") == 1


class TestMarkUrl:
    def test_transitions_pending_to_added(self, tmp_path: Path) -> None:
        conn = make_db(tmp_path)
        state.upsert_pending(conn, ["https://x.com"])
        state.mark_url(conn, "https://x.com", "added")
        row = conn.execute("SELECT status FROM articles WHERE url = ?", ("https://x.com",)).fetchone()
        assert row[0] == "added"

    def test_transitions_pending_to_skipped(self, tmp_path: Path) -> None:
        conn = make_db(tmp_path)
        state.upsert_pending(conn, ["https://x.com"])
        state.mark_url(conn, "https://x.com", "skipped")
        row = conn.execute("SELECT status FROM articles WHERE url = ?", ("https://x.com",)).fetchone()
        assert row[0] == "skipped"

    def test_raises_for_unknown_url(self, tmp_path: Path) -> None:
        conn = make_db(tmp_path)
        with pytest.raises(ValueError, match="not found in state DB"):
            state.mark_url(conn, "https://nope.com", "added")

    def test_updates_updated_at_on_transition(self, tmp_path: Path) -> None:
        conn = make_db(tmp_path)
        state.upsert_pending(conn, ["https://x.com"])
        before: str = conn.execute(
            "SELECT updated_at FROM articles WHERE url = ?", ("https://x.com",)
        ).fetchone()[0]
        state.mark_url(conn, "https://x.com", "added")
        after: str = conn.execute(
            "SELECT updated_at FROM articles WHERE url = ?", ("https://x.com",)
        ).fetchone()[0]
        assert after >= before


class TestGetByStatus:
    def test_returns_articles_with_matching_status(self, tmp_path: Path) -> None:
        conn = make_db(tmp_path)
        state.upsert_pending(conn, ["https://a.com", "https://b.com"])
        state.mark_url(conn, "https://a.com", "added")
        results = state.get_by_status(conn, "pending")
        assert len(results) == 1
        assert results[0]["url"] == "https://b.com"

    def test_returns_empty_list_when_none_match(self, tmp_path: Path) -> None:
        conn = make_db(tmp_path)
        assert state.get_by_status(conn, "added") == []

    def test_record_has_all_required_fields(self, tmp_path: Path) -> None:
        conn = make_db(tmp_path)
        state.upsert_pending(conn, ["https://x.com"])
        records = state.get_by_status(conn, "pending")
        assert set(records[0].keys()) == {"url", "status", "first_seen_at", "updated_at"}


class TestGetStats:
    def test_returns_zero_counts_for_empty_db(self, tmp_path: Path) -> None:
        conn = make_db(tmp_path)
        assert state.get_stats(conn) == {"pending": 0, "added": 0, "skipped": 0}

    def test_counts_all_states_accurately(self, tmp_path: Path) -> None:
        conn = make_db(tmp_path)
        state.upsert_pending(conn, ["https://a.com", "https://b.com", "https://c.com", "https://d.com"])
        state.mark_url(conn, "https://a.com", "added")
        state.mark_url(conn, "https://b.com", "skipped")
        assert state.get_stats(conn) == {"pending": 2, "added": 1, "skipped": 1}
