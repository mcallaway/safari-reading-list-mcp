from datetime import UTC, datetime

import plistlib
import pytest

from safari_reading_list_mcp.safari_bookmarks import read_reading_list_items


def test_read_reading_list_items_from_plist(tmp_path) -> None:
    bookmarks = {
        "Title": "Root",
        "Children": [
            {
                "Title": "com.apple.ReadingList",
                "Children": [
                    {
                        "URLString": "https://example.com/1",
                        "URIDictionary": {"title": "Example One"},
                        "ReadingList": {
                            "DateAdded": datetime(2026, 4, 5, 0, 0, 0, tzinfo=UTC),
                            "PreviewText": "Preview one",
                        },
                    }
                ],
            }
        ],
    }
    plist_path = tmp_path / "Bookmarks.plist"
    with plist_path.open("wb") as file:
        plistlib.dump(bookmarks, file)

    items = read_reading_list_items(plist_path)

    assert len(items) == 1
    assert items[0].title == "Example One"
    assert items[0].url == "https://example.com/1"
    assert items[0].preview_text == "Preview one"


def test_read_reading_list_items_raises_when_missing_container(tmp_path) -> None:
    bookmarks = {"Title": "Root", "Children": []}
    plist_path = tmp_path / "Bookmarks.plist"
    with plist_path.open("wb") as file:
        plistlib.dump(bookmarks, file)

    with pytest.raises(ValueError):
        read_reading_list_items(plist_path)
