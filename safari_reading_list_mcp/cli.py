from __future__ import annotations

import json

import click

from .server import mcp
from .service import export_reading_list


@click.group()
def main() -> None:
    """Safari Reading List MCP utility CLI."""


@main.group("export")
def export_group() -> None:
    """Export Safari Reading List entries to JSON."""


def _render_export_result(result: dict[str, object]) -> None:
    click.echo(f"success: {result['success']}")
    click.echo(f"output_path: {result['output_path']}")
    click.echo(f"exported_count: {result['exported_count']}")
    click.echo(f"total_count: {result['total_count']}")
    click.echo(f"filters_applied: {json.dumps(result['filters_applied'])}")
    warnings = result.get("warnings", [])
    if warnings:
        click.echo(f"warnings: {json.dumps(warnings)}")


@export_group.command("week")
@click.option("--output", "output_path", required=True, help="Path to output JSON file.")
@click.option(
    "--bookmarks-path",
    default=None,
    help="Optional override for Safari Bookmarks.plist path.",
)
def export_week(output_path: str, bookmarks_path: str | None) -> None:
    """Export entries from the past 7 days (default behavior)."""
    result = export_reading_list(
        output_path=output_path,
        bookmarks_path=bookmarks_path,
    )
    _render_export_result(result)


@export_group.command("range")
@click.option("--start", "start_time", required=True, help="RFC 3339 start datetime.")
@click.option("--end", "end_time", required=True, help="RFC 3339 end datetime.")
@click.option("--output", "output_path", required=True, help="Path to output JSON file.")
@click.option(
    "--bookmarks-path",
    default=None,
    help="Optional override for Safari Bookmarks.plist path.",
)
def export_range(
    start_time: str,
    end_time: str,
    output_path: str,
    bookmarks_path: str | None,
) -> None:
    """Export entries for an explicit inclusive time range."""
    result = export_reading_list(
        output_path=output_path,
        start_time=start_time,
        end_time=end_time,
        bookmarks_path=bookmarks_path,
    )
    _render_export_result(result)


@export_group.command("all")
@click.option("--output", "output_path", required=True, help="Path to output JSON file.")
@click.option(
    "--bookmarks-path",
    default=None,
    help="Optional override for Safari Bookmarks.plist path.",
)
def export_all(output_path: str, bookmarks_path: str | None) -> None:
    """Export all Reading List entries."""
    result = export_reading_list(
        output_path=output_path,
        full_export=True,
        bookmarks_path=bookmarks_path,
    )
    _render_export_result(result)


@main.command("serve")
@click.option(
    "--transport",
    type=click.Choice(["stdio", "streamable-http", "sse"]),
    default="stdio",
    show_default=True,
    help="MCP transport mode.",
)
def serve(transport: str) -> None:
    """Run the MCP server."""
    mcp.run(transport=transport)
