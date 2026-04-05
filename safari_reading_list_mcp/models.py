from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(slots=True)
class ReadingListItem:
    title: str
    url: str
    date_added: str | None
    preview_text: str | None

    def to_dict(self) -> dict[str, str | None]:
        return asdict(self)
