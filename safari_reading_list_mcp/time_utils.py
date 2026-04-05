from __future__ import annotations

from datetime import UTC, datetime, timedelta


def parse_rfc3339(value: str) -> datetime:
    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"

    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError(
            f"Invalid RFC 3339 datetime: {value!r}. Expected values like '2026-04-05T00:00:00Z'."
        ) from exc

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)

    return parsed.astimezone(UTC)


def default_week_range(now: datetime) -> tuple[datetime, datetime]:
    if now.tzinfo is None:
        now = now.replace(tzinfo=UTC)
    now_utc = now.astimezone(UTC)
    return now_utc - timedelta(days=7), now_utc


def resolve_effective_range(
    *,
    start_time: str | None,
    end_time: str | None,
    full_export: bool,
    now: datetime,
) -> tuple[datetime | None, datetime | None, bool]:
    if full_export:
        return None, None, False

    if start_time is None and end_time is None:
        start, end = default_week_range(now)
        return start, end, True

    end = parse_rfc3339(end_time) if end_time else now.astimezone(UTC)
    start = parse_rfc3339(start_time) if start_time else (end - timedelta(days=7))

    if start > end:
        raise ValueError("Invalid time range: start_time must be less than or equal to end_time.")

    return start, end, False
