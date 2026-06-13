from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import TypedDict

from . import state as state_mod
from .exporter import export_to_json, filter_items_by_range
from .safari_bookmarks import read_reading_list_items
from .time_utils import resolve_effective_range

DEFAULT_BOOKMARKS_PATH = Path("~/Library/Safari/Bookmarks.plist").expanduser()


class ExportFilters(TypedDict, total=False):
    full_export: bool
    start_time: str
    end_time: str
    default_range: bool


class ExportResult(TypedDict):
    success: bool
    output_path: str
    exported_count: int
    total_count: int
    filters_applied: ExportFilters
    warnings: list[str]
    error: str | None
    new_to_db: int
    already_added: int
    already_skipped: int


def export_reading_list(
    *,
    output_path: str,
    start_time: str | None = None,
    end_time: str | None = None,
    full_export: bool = False,
    bookmarks_path: str | None = None,
    state_db_path: str | None = None,
    unprocessed_only: bool = False,
    now: datetime | None = None,
) -> ExportResult:
    if unprocessed_only and state_db_path is None:
        raise ValueError("state_db_path is required when unprocessed_only is True.")

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
        candidate_items = items
        filters_applied: ExportFilters = {"full_export": True}
    else:
        assert effective_start is not None and effective_end is not None
        candidate_items, range_warnings = filter_items_by_range(items, effective_start, effective_end)
        warnings.extend(range_warnings)
        filters_applied = {
            "start_time": effective_start.isoformat().replace("+00:00", "Z"),
            "end_time": effective_end.isoformat().replace("+00:00", "Z"),
            "default_range": defaulted,
        }

    new_to_db = 0
    already_added = 0
    already_skipped = 0

    if state_db_path is not None:
        candidate_urls = [item.url for item in candidate_items]
        conn = state_mod.open_db(Path(state_db_path).expanduser())
        try:
            already_added = state_mod.count_by_status(conn, candidate_urls, "added")
            already_skipped = state_mod.count_by_status(conn, candidate_urls, "skipped")
            new_to_db = state_mod.upsert_pending(conn, candidate_urls)
            if unprocessed_only:
                unprocessed_urls = set(state_mod.filter_unprocessed(conn, candidate_urls))
                candidate_items = [i for i in candidate_items if i.url in unprocessed_urls]
        finally:
            conn.close()

    export_to_json(candidate_items, output)

    return {
        "success": True,
        "output_path": str(output),
        "exported_count": len(candidate_items),
        "total_count": total_count,
        "filters_applied": filters_applied,
        "warnings": warnings,
        "error": None,
        "new_to_db": new_to_db,
        "already_added": already_added,
        "already_skipped": already_skipped,
    }
