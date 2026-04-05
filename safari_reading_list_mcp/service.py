from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from .exporter import export_to_json, filter_items_by_range
from .safari_bookmarks import read_reading_list_items
from .time_utils import resolve_effective_range

DEFAULT_BOOKMARKS_PATH = Path("~/Library/Safari/Bookmarks.plist").expanduser()


def export_reading_list(
    *,
    output_path: str,
    start_time: str | None = None,
    end_time: str | None = None,
    full_export: bool = False,
    bookmarks_path: str | None = None,
    now: datetime | None = None,
) -> dict[str, object]:
    now_value = now or datetime.now(tz=UTC)
    bookmarks = Path(bookmarks_path).expanduser() if bookmarks_path else DEFAULT_BOOKMARKS_PATH
    output = Path(output_path).expanduser()

    items = read_reading_list_items(bookmarks)
    total_count = len(items)

    effective_start, effective_end, defaulted = resolve_effective_range(
        start_time=start_time,
        end_time=end_time,
        full_export=full_export,
        now=now_value,
    )

    warnings: list[str] = []
    if full_export:
        exported_items = items
        filters_applied: dict[str, object] = {"full_export": True}
    else:
        assert effective_start is not None and effective_end is not None
        exported_items, range_warnings = filter_items_by_range(items, effective_start, effective_end)
        warnings.extend(range_warnings)
        filters_applied = {
            "start_time": effective_start.isoformat().replace("+00:00", "Z"),
            "end_time": effective_end.isoformat().replace("+00:00", "Z"),
            "default_range": defaulted,
        }

    export_to_json(exported_items, output)

    return {
        "success": True,
        "output_path": str(output),
        "exported_count": len(exported_items),
        "total_count": total_count,
        "filters_applied": filters_applied,
        "warnings": warnings,
    }
