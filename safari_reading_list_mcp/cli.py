from __future__ import annotations

import logging

import click

from .server import mcp
from .service import export_reading_list

logger = logging.getLogger(__name__)


def _configure_logging(log_level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.WARNING),
        format="%(levelname)s %(name)s: %(message)s",
        force=True,
    )


@click.group()
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], case_sensitive=False),
    default="WARNING",
    show_default=True,
    help="Set logging verbosity for human-readable messages (stderr).",
)
def main(log_level: str) -> None:
    """Safari Reading List MCP utility CLI."""
    _configure_logging(log_level)


@main.group("export")
def export_group() -> None:
    """Export Safari Reading List entries to JSON."""


def _log_export_result(result: dict[str, object]) -> None:
    logger.info("success=%s", result["success"])
    logger.info("output_path=%s", result["output_path"])
    logger.info("exported_count=%s", result["exported_count"])
    logger.info("total_count=%s", result["total_count"])
    logger.debug("filters_applied=%s", result["filters_applied"])
    warnings = result.get("warnings", [])
    if warnings:
        for warning in warnings:
            logger.warning("%s", warning)


def _run_export(**kwargs: object) -> None:
    try:
        result = export_reading_list(**kwargs)
    except Exception as exc:  # noqa: BLE001
        logger.error("Export failed: %s", exc)
        raise click.ClickException(str(exc)) from exc

    _log_export_result(result)


@export_group.command("week")
@click.option("--output", "output_path", required=True, help="Path to output JSON file.")
@click.option(
    "--bookmarks-path",
    default=None,
    help="Optional override for Safari Bookmarks.plist path.",
)
def export_week(output_path: str, bookmarks_path: str | None) -> None:
    """Export entries from the past 7 days (default behavior)."""
    _run_export(
        output_path=output_path,
        bookmarks_path=bookmarks_path,
    )


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
    _run_export(
        output_path=output_path,
        start_time=start_time,
        end_time=end_time,
        bookmarks_path=bookmarks_path,
    )


@export_group.command("all")
@click.option("--output", "output_path", required=True, help="Path to output JSON file.")
@click.option(
    "--bookmarks-path",
    default=None,
    help="Optional override for Safari Bookmarks.plist path.",
)
def export_all(output_path: str, bookmarks_path: str | None) -> None:
    """Export all Reading List entries."""
    _run_export(
        output_path=output_path,
        full_export=True,
        bookmarks_path=bookmarks_path,
    )


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
    logger.warning("Starting MCP server with transport=%s", transport)
    mcp.run(transport=transport)
