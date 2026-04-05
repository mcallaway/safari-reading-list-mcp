from datetime import UTC, datetime

import pytest

from safari_reading_list_mcp.exporter import export_to_json, filter_items_by_range
from safari_reading_list_mcp.models import ReadingListItem


def test_filter_items_by_range_inclusive() -> None:
    items = [
        ReadingListItem("A", "https://a", "2026-04-01T00:00:00Z", None),
        ReadingListItem("B", "https://b", "2026-04-02T00:00:00Z", None),
        ReadingListItem("C", "https://c", "2026-04-03T00:00:00Z", None),
    ]
    start = datetime(2026, 4, 2, 0, 0, 0, tzinfo=UTC)
    end = datetime(2026, 4, 3, 0, 0, 0, tzinfo=UTC)

    filtered, warnings = filter_items_by_range(items, start, end)

    assert [x.title for x in filtered] == ["B", "C"]
    assert warnings == []


def test_filter_items_by_range_raises_when_all_dates_missing() -> None:
    items = [
        ReadingListItem("A", "https://a", None, None),
        ReadingListItem("B", "https://b", None, None),
    ]
    with pytest.raises(ValueError):
        filter_items_by_range(
            items,
            datetime(2026, 4, 1, 0, 0, 0, tzinfo=UTC),
            datetime(2026, 4, 5, 0, 0, 0, tzinfo=UTC),
        )


def test_export_to_json_writes_file(tmp_path) -> None:
    output_file = tmp_path / "reading-list.json"
    items = [
        ReadingListItem("A", "https://a", "2026-04-01T00:00:00Z", "preview")
    ]

    export_to_json(items, output_file)

    assert output_file.exists()
    text = output_file.read_text(encoding="utf-8")
    assert '"title": "A"' in text
    assert '"url": "https://a"' in text
