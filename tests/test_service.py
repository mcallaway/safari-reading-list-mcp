from datetime import UTC, datetime

import plistlib

from safari_reading_list_mcp.service import export_reading_list


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
    assert result["filters_applied"]["default_range"] is True
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
