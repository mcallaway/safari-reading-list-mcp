from datetime import UTC, datetime
from pathlib import Path

import plistlib
import pytest

from safari_reading_list_mcp.service import export_reading_list
from safari_reading_list_mcp import state


def _write_sample_bookmarks(path):
    bookmarks = {
        "Title": "Root",
        "Children": [
            {
                "Title": "com.apple.ReadingList",
                "Children": [
                    {
                        "URLString": "https://example.com/old",
                        "URIDictionary": {"title": "Old"},
                        "ReadingList": {
                            "DateAdded": datetime(2026, 3, 20, 0, 0, 0, tzinfo=UTC),
                        },
                    },
                    {
                        "URLString": "https://example.com/new",
                        "URIDictionary": {"title": "New"},
                        "ReadingList": {
                            "DateAdded": datetime(2026, 4, 4, 0, 0, 0, tzinfo=UTC),
                        },
                    },
                ],
            }
        ],
    }
    with path.open("wb") as file:
        plistlib.dump(bookmarks, file)


def test_export_reading_list_defaults_to_last_week(tmp_path) -> None:
    plist_path = tmp_path / "Bookmarks.plist"
    _write_sample_bookmarks(plist_path)
    output = tmp_path / "week.json"

    result = export_reading_list(
        output_path=str(output),
        bookmarks_path=str(plist_path),
        now=datetime(2026, 4, 5, 0, 0, 0, tzinfo=UTC),
    )

    assert result["success"] is True
    assert result["total_count"] == 2
    assert result["exported_count"] == 1
    assert result["filters_applied"].get("default_range") is True
    assert output.exists()


def test_export_reading_list_full_export(tmp_path) -> None:
    plist_path = tmp_path / "Bookmarks.plist"
    _write_sample_bookmarks(plist_path)
    output = tmp_path / "all.json"

    result = export_reading_list(
        output_path=str(output),
        bookmarks_path=str(plist_path),
        full_export=True,
        now=datetime(2026, 4, 5, 0, 0, 0, tzinfo=UTC),
    )

    assert result["success"] is True
    assert result["exported_count"] == 2
    assert result["filters_applied"] == {"full_export": True}


def test_export_without_state_db_has_zero_state_counts(tmp_path: Path) -> None:
    plist_path = tmp_path / "Bookmarks.plist"
    _write_sample_bookmarks(plist_path)
    output = tmp_path / "out.json"

    result = export_reading_list(
        output_path=str(output),
        bookmarks_path=str(plist_path),
        full_export=True,
        now=datetime(2026, 4, 5, 0, 0, 0, tzinfo=UTC),
    )

    assert result["new_to_db"] == 0
    assert result["already_added"] == 0
    assert result["already_skipped"] == 0


def test_export_with_state_db_upserts_urls_as_pending(tmp_path: Path) -> None:
    plist_path = tmp_path / "Bookmarks.plist"
    _write_sample_bookmarks(plist_path)
    db_path = tmp_path / "state.db"
    output = tmp_path / "out.json"

    result = export_reading_list(
        output_path=str(output),
        bookmarks_path=str(plist_path),
        full_export=True,
        state_db_path=str(db_path),
        now=datetime(2026, 4, 5, 0, 0, 0, tzinfo=UTC),
    )

    assert result["new_to_db"] == 2
    conn = state.open_db(db_path)
    stats = state.get_stats(conn)
    conn.close()
    assert stats["pending"] == 2


def test_export_state_counts_already_added_and_skipped(tmp_path: Path) -> None:
    plist_path = tmp_path / "Bookmarks.plist"
    _write_sample_bookmarks(plist_path)
    db_path = tmp_path / "state.db"
    output = tmp_path / "out.json"

    # Pre-populate state: mark one added, one skipped
    conn = state.open_db(db_path)
    state.upsert_pending(conn, ["https://example.com/old", "https://example.com/new"])
    state.mark_url(conn, "https://example.com/old", "added")
    state.mark_url(conn, "https://example.com/new", "skipped")
    conn.close()

    result = export_reading_list(
        output_path=str(output),
        bookmarks_path=str(plist_path),
        full_export=True,
        state_db_path=str(db_path),
        now=datetime(2026, 4, 5, 0, 0, 0, tzinfo=UTC),
    )

    assert result["new_to_db"] == 0
    assert result["already_added"] == 1
    assert result["already_skipped"] == 1


def test_export_unprocessed_only_excludes_terminal_items(tmp_path: Path) -> None:
    plist_path = tmp_path / "Bookmarks.plist"
    _write_sample_bookmarks(plist_path)
    db_path = tmp_path / "state.db"
    output = tmp_path / "out.json"

    # Mark old as added — it should not appear in unprocessed export
    conn = state.open_db(db_path)
    state.upsert_pending(conn, ["https://example.com/old"])
    state.mark_url(conn, "https://example.com/old", "added")
    conn.close()

    result = export_reading_list(
        output_path=str(output),
        bookmarks_path=str(plist_path),
        full_export=True,
        state_db_path=str(db_path),
        unprocessed_only=True,
        now=datetime(2026, 4, 5, 0, 0, 0, tzinfo=UTC),
    )

    assert result["exported_count"] == 1
    assert result["total_count"] == 2


def test_export_unprocessed_only_without_state_db_raises(tmp_path: Path) -> None:
    plist_path = tmp_path / "Bookmarks.plist"
    _write_sample_bookmarks(plist_path)
    output = tmp_path / "out.json"

    with pytest.raises(ValueError, match="state_db_path is required"):
        export_reading_list(
            output_path=str(output),
            bookmarks_path=str(plist_path),
            full_export=True,
            unprocessed_only=True,
            now=datetime(2026, 4, 5, 0, 0, 0, tzinfo=UTC),
        )
