from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .service import ExportResult, export_reading_list

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
        }


def run_server() -> None:
    mcp.run(transport="stdio")
