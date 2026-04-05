from __future__ import annotations

import plistlib
from datetime import datetime
from pathlib import Path
from typing import Any

from .models import ReadingListItem


def load_bookmarks_root(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Safari bookmarks file not found: {path}")

    with path.open("rb") as file:
        loaded = plistlib.load(file)

    if not isinstance(loaded, dict):
        raise ValueError("Safari bookmarks plist has an unexpected structure.")

    return loaded


def find_reading_list_container(node: Any) -> dict[str, Any] | None:
    if not isinstance(node, dict):
        return None

    title = node.get("Title")
    if title in {"com.apple.ReadingList", "Reading List"}:
        return node

    for child in node.get("Children", []):
        found = find_reading_list_container(child)
        if found is not None:
            return found

    return None


def iter_leaf_bookmarks(node: Any):
    if not isinstance(node, dict):
        return

    children = node.get("Children")
    if isinstance(children, list):
        for child in children:
            yield from iter_leaf_bookmarks(child)
        return

    if "URLString" in node:
        yield node


def normalize_date(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.isoformat()
    return str(value)


def extract_reading_list_items(container: dict[str, Any]) -> list[ReadingListItem]:
    items: list[ReadingListItem] = []

    for leaf in iter_leaf_bookmarks(container):
        url = leaf.get("URLString")
        if not url:
            continue

        uri_dict = leaf.get("URIDictionary") or {}
        title = uri_dict.get("title") or leaf.get("Title") or url

        metadata = leaf.get("ReadingList") or {}
        date_added = normalize_date(
            metadata.get("DateAdded")
            or metadata.get("Date Added")
            or leaf.get("DateAdded")
        )
        preview = metadata.get("PreviewText") or metadata.get("Preview Text")

        items.append(
            ReadingListItem(
                title=str(title),
                url=str(url),
                date_added=date_added,
                preview_text=str(preview) if preview else None,
            )
        )

    items.sort(key=lambda item: item.date_added or "", reverse=True)
    return items


def read_reading_list_items(bookmarks_path: Path) -> list[ReadingListItem]:
    root = load_bookmarks_root(bookmarks_path)
    container = find_reading_list_container(root)
    if container is None:
        raise ValueError("Could not locate Safari Reading List container in bookmarks data.")
    return extract_reading_list_items(container)
