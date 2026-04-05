from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from .models import ReadingListItem
from .time_utils import parse_rfc3339


def filter_items_by_range(
    items: list[ReadingListItem],
    start: datetime,
    end: datetime,
) -> tuple[list[ReadingListItem], list[str]]:
    warnings: list[str] = []
    filtered: list[ReadingListItem] = []
    missing_dates = 0

    for item in items:
        if not item.date_added:
            missing_dates += 1
            continue

        try:
            added = parse_rfc3339(item.date_added)
        except ValueError:
            missing_dates += 1
            continue

        if start <= added <= end:
            filtered.append(item)

    if missing_dates == len(items) and items:
        raise ValueError(
            "Date-range filtering unavailable: Safari Reading List entries do not include parseable timestamps."
        )

    if missing_dates:
        warnings.append(
            f"Excluded {missing_dates} entries that did not include parseable date metadata."
        )

    return filtered, warnings


def export_to_json(items: list[ReadingListItem], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = [item.to_dict() for item in items]
    output_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
