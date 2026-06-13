from pathlib import Path

import pytest

from safari_reading_list_mcp import server
from safari_reading_list_mcp import state


def test_export_reading_list_tool_surfaces_error(monkeypatch) -> None:
    def boom(**_kwargs):
        raise ValueError("bad range")

    monkeypatch.setattr(server, "export_reading_list", boom)

    result = server.export_reading_list_tool(output_path="/tmp/x.json")

    assert result["success"] is False
    assert result["error"] == "bad range"
    assert result["exported_count"] == 0


def test_export_reading_list_tool_success_shape(monkeypatch) -> None:
    def fake_export(**_kwargs):
        return {
            "success": True,
            "output_path": "/tmp/x.json",
            "exported_count": 1,
            "total_count": 2,
            "filters_applied": {"default_range": True},
            "warnings": [],
            "new_to_db": 1,
            "already_added": 0,
            "already_skipped": 0,
        }

    monkeypatch.setattr(server, "export_reading_list", fake_export)

    result = server.export_reading_list_tool(output_path="/tmp/x.json")

    assert result["success"] is True
    assert result["exported_count"] == 1
    assert "filters_applied" in result


@pytest.mark.req("state-tracking.MCP.1")
def test_list_reading_list_state_tool_returns_records(tmp_path: Path) -> None:
    db_path = tmp_path / "state.db"
    conn = state.open_db(db_path)
    state.upsert_pending(conn, ["https://a.com", "https://b.com"])
    state.mark_url(conn, "https://a.com", "added")
    conn.close()

    result = server.list_reading_list_state_tool(
        status="pending",
        state_db_path=str(db_path),
    )

    assert result["success"] is True
    assert len(result["records"]) == 1
    assert result["records"][0]["url"] == "https://b.com"
    assert result["records"][0]["status"] == "pending"


@pytest.mark.req("state-tracking.MCP.2")
def test_list_reading_list_state_tool_all_statuses(tmp_path: Path) -> None:
    db_path = tmp_path / "state.db"
    conn = state.open_db(db_path)
    state.upsert_pending(conn, ["https://a.com", "https://b.com"])
    conn.close()

    result = server.list_reading_list_state_tool(state_db_path=str(db_path))

    assert result["success"] is True
    assert len(result["records"]) == 2


@pytest.mark.req("state-tracking.MCP.3")
def test_mark_reading_list_item_tool_transitions_state(tmp_path: Path) -> None:
    db_path = tmp_path / "state.db"
    conn = state.open_db(db_path)
    state.upsert_pending(conn, ["https://x.com"])
    conn.close()

    result = server.mark_reading_list_item_tool(
        url="https://x.com",
        status="added",
        state_db_path=str(db_path),
    )

    assert result["success"] is True

    conn = state.open_db(db_path)
    records = state.get_by_status(conn, "added")
    conn.close()
    assert len(records) == 1


@pytest.mark.req("state-tracking.MCP.4")
def test_mark_reading_list_item_tool_unknown_url_returns_error(tmp_path: Path) -> None:
    db_path = tmp_path / "state.db"
    state.open_db(db_path).close()

    result = server.mark_reading_list_item_tool(
        url="https://ghost.com",
        status="skipped",
        state_db_path=str(db_path),
    )

    assert result["success"] is False
    assert "not found" in result["error"]


def test_list_reading_list_state_tool_invalid_status_returns_error(tmp_path: Path) -> None:
    db_path = tmp_path / "state.db"
    state.open_db(db_path).close()

    result = server.list_reading_list_state_tool(
        status="done",
        state_db_path=str(db_path),
    )

    assert result["success"] is False
    assert "Invalid status" in result["error"]


def test_mark_reading_list_item_tool_invalid_status_returns_error(tmp_path: Path) -> None:
    db_path = tmp_path / "state.db"
    state.open_db(db_path).close()

    result = server.mark_reading_list_item_tool(
        url="https://x.com",
        status="done",
        state_db_path=str(db_path),
    )

    assert result["success"] is False
    assert "Invalid status" in result["error"]
