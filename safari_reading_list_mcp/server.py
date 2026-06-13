from __future__ import annotations

from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

from . import state as state_mod
from .service import ExportResult, export_reading_list
from .state import DEFAULT_DB_PATH, ArticleRecord

mcp = FastMCP("safari-reading-list-mcp")


@mcp.tool(
    name="export_reading_list",
    description=(
        "Export Safari Reading List entries to a JSON file. "
        "Defaults to the last 7 days unless full_export is true or a custom range is provided."
    ),
)
def export_reading_list_tool(
    output_path: str,
    start_time: str | None = None,
    end_time: str | None = None,
    full_export: bool = False,
) -> ExportResult:
    try:
        return export_reading_list(
            output_path=output_path,
            start_time=start_time,
            end_time=end_time,
            full_export=full_export,
        )
    except Exception as exc:  # noqa: BLE001
        return {
            "success": False,
            "output_path": output_path,
            "exported_count": 0,
            "total_count": 0,
            "filters_applied": {},
            "warnings": [],
            "error": str(exc),
            "new_to_db": 0,
            "already_added": 0,
            "already_skipped": 0,
        }


def _state_error(message: str) -> dict[str, Any]:
    return {"success": False, "error": message, "records": []}


_VALID_STATUSES = frozenset({"pending", "added", "skipped"})


@mcp.tool(
    name="list_reading_list_state",
    description=(
        "List Reading List articles by processing state. "
        "status: 'pending' (default), 'added', or 'skipped'."
    ),
)
def list_reading_list_state_tool(
    status: str | None = None,
    state_db_path: str | None = None,
) -> dict[str, Any]:
    effective_status = status or "pending"
    if effective_status not in _VALID_STATUSES:
        return _state_error(f"Invalid status {effective_status!r}. Must be one of: pending, added, skipped.")
    db = Path(state_db_path).expanduser() if state_db_path else DEFAULT_DB_PATH
    conn = state_mod.open_db(db)
    try:
        records: list[ArticleRecord] = state_mod.get_by_status(
            conn, effective_status  # type: ignore[arg-type]
        )
    except Exception as exc:  # noqa: BLE001
        return _state_error(str(exc))
    finally:
        conn.close()
    return {"success": True, "error": None, "records": records}


@mcp.tool(
    name="mark_reading_list_item",
    description="Mark a Reading List URL as 'added' (incorporated into Second Brain) or 'skipped'.",
)
def mark_reading_list_item_tool(
    url: str,
    status: str,
    state_db_path: str | None = None,
) -> dict[str, Any]:
    if status not in {"added", "skipped"}:
        return {"success": False, "error": f"Invalid status {status!r}. Must be 'added' or 'skipped'."}
    db = Path(state_db_path).expanduser() if state_db_path else DEFAULT_DB_PATH
    conn = state_mod.open_db(db)
    try:
        state_mod.mark_url(conn, url, status)  # type: ignore[arg-type]
    except ValueError as exc:
        return {"success": False, "error": str(exc)}
    except Exception as exc:  # noqa: BLE001
        return {"success": False, "error": str(exc)}
    finally:
        conn.close()
    return {"success": True, "error": None}


def run_server() -> None:
    mcp.run(transport="stdio")
