from datetime import UTC, datetime

import pytest

from safari_reading_list_mcp.time_utils import (
    default_week_range,
    parse_rfc3339,
    resolve_effective_range,
)


def test_parse_rfc3339_accepts_z_suffix() -> None:
    value = parse_rfc3339("2026-04-05T00:00:00Z")
    assert value == datetime(2026, 4, 5, 0, 0, 0, tzinfo=UTC)


def test_parse_rfc3339_rejects_invalid() -> None:
    with pytest.raises(ValueError):
        parse_rfc3339("2026/04/05")


def test_default_week_range_is_seven_days() -> None:
    now = datetime(2026, 4, 5, 12, 0, 0, tzinfo=UTC)
    start, end = default_week_range(now)
    assert end == now
    assert (end - start).days == 7


def test_resolve_effective_range_defaults_to_week() -> None:
    now = datetime(2026, 4, 5, 12, 0, 0, tzinfo=UTC)
    start, end, defaulted = resolve_effective_range(
        start_time=None,
        end_time=None,
        full_export=False,
        now=now,
    )
    assert defaulted is True
    assert end == now
    assert (end - start).days == 7


def test_resolve_effective_range_rejects_inverted_range() -> None:
    with pytest.raises(ValueError):
        resolve_effective_range(
            start_time="2026-04-06T00:00:00Z",
            end_time="2026-04-05T00:00:00Z",
            full_export=False,
            now=datetime(2026, 4, 7, 0, 0, 0, tzinfo=UTC),
        )
