from __future__ import annotations

import logging
from pathlib import Path
from typing import Literal

import click

from .server import mcp
from .service import ExportResult, export_reading_list
from . import state as state_mod

logger = logging.getLogger(__name__)

_DEFAULT_DB_PATH = str(Path("~/.local/share/srl/state.db").expanduser())


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


def _log_export_result(result: ExportResult) -> None:
    logger.info("success=%s", result["success"])
    logger.info("output_path=%s", result["output_path"])
    logger.info("exported_count=%s", result["exported_count"])
    logger.info("total_count=%s", result["total_count"])
    logger.info("new_to_db=%s", result["new_to_db"])
    logger.info("already_added=%s", result["already_added"])
    logger.info("already_skipped=%s", result["already_skipped"])
    logger.debug("filters_applied=%s", result["filters_applied"])
    for warning in result["warnings"]:
        logger.warning("%s", warning)


def _run_export(
    *,
    output_path: str,
    start_time: str | None = None,
    end_time: str | None = None,
    full_export: bool = False,
    bookmarks_path: str | None = None,
    state_db_path: str | None = None,
    unprocessed_only: bool = False,
) -> None:
    try:
        result = export_reading_list(
            output_path=output_path,
            start_time=start_time,
            end_time=end_time,
            full_export=full_export,
            bookmarks_path=bookmarks_path,
            state_db_path=state_db_path,
            unprocessed_only=unprocessed_only,
        )
    except Exception as exc:  # noqa: BLE001
        logger.error("Export failed: %s", exc)
        raise click.ClickException(str(exc)) from exc

    _log_export_result(result)


_db_path_option = click.option(
    "--db-path",
    "state_db_path",
    default=_DEFAULT_DB_PATH,
    envvar="SRL_STATE_DB",
    show_default=True,
    help="Path to the state SQLite DB.",
)
_unprocessed_only_option = click.option(
    "--unprocessed-only",
    is_flag=True,
    default=False,
    help="Only export items not yet marked added or skipped.",
)
_bookmarks_path_option = click.option(
    "--bookmarks-path",
    default=None,
    help="Optional override for Safari Bookmarks.plist path.",
)


@export_group.command("week")
@click.option("--output", "output_path", required=True, help="Path to output JSON file.")
@_bookmarks_path_option
@_db_path_option
@_unprocessed_only_option
def export_week(
    output_path: str,
    bookmarks_path: str | None,
    state_db_path: str,
    unprocessed_only: bool,
) -> None:
    """Export entries from the past 7 days (default behavior)."""
    _run_export(
        output_path=output_path,
        bookmarks_path=bookmarks_path,
        state_db_path=state_db_path,
        unprocessed_only=unprocessed_only,
    )


@export_group.command("range")
@click.option("--start", "start_time", required=True, help="RFC 3339 start datetime.")
@click.option("--end", "end_time", required=True, help="RFC 3339 end datetime.")
@click.option("--output", "output_path", required=True, help="Path to output JSON file.")
@_bookmarks_path_option
@_db_path_option
@_unprocessed_only_option
def export_range(
    start_time: str,
    end_time: str,
    output_path: str,
    bookmarks_path: str | None,
    state_db_path: str,
    unprocessed_only: bool,
) -> None:
    """Export entries for an explicit inclusive time range."""
    _run_export(
        output_path=output_path,
        start_time=start_time,
        end_time=end_time,
        bookmarks_path=bookmarks_path,
        state_db_path=state_db_path,
        unprocessed_only=unprocessed_only,
    )


@export_group.command("all")
@click.option("--output", "output_path", required=True, help="Path to output JSON file.")
@_bookmarks_path_option
@_db_path_option
@_unprocessed_only_option
def export_all(
    output_path: str,
    bookmarks_path: str | None,
    state_db_path: str,
    unprocessed_only: bool,
) -> None:
    """Export all Reading List entries."""
    _run_export(
        output_path=output_path,
        full_export=True,
        bookmarks_path=bookmarks_path,
        state_db_path=state_db_path,
        unprocessed_only=unprocessed_only,
    )


@main.group("state")
def state_group() -> None:
    """Query and update article processing state."""


@state_group.command("stats")
@click.option(
    "--db-path",
    "state_db_path",
    default=_DEFAULT_DB_PATH,
    envvar="SRL_STATE_DB",
    show_default=True,
    help="Path to the state SQLite DB.",
)
def state_stats(state_db_path: str) -> None:
    """Show count of articles per state."""
    try:
        conn = state_mod.open_db(Path(state_db_path).expanduser())
        stats = state_mod.get_stats(conn)
        conn.close()
    except Exception as exc:  # noqa: BLE001
        raise click.ClickException(str(exc)) from exc

    for status in ("pending", "added", "skipped"):
        click.echo(f"{status:<10} {stats[status]}")


@state_group.command("list")
@click.option(
    "--status",
    type=click.Choice(["pending", "added", "skipped"]),
    default="pending",
    show_default=True,
    help="Filter articles by state.",
)
@click.option(
    "--db-path",
    "state_db_path",
    default=_DEFAULT_DB_PATH,
    envvar="SRL_STATE_DB",
    show_default=True,
    help="Path to the state SQLite DB.",
)
def state_list(status: str, state_db_path: str) -> None:
    """List articles by state (default: pending)."""
    try:
        conn = state_mod.open_db(Path(state_db_path).expanduser())
        records = state_mod.get_by_status(conn, status)  # type: ignore[arg-type]
        conn.close()
    except Exception as exc:  # noqa: BLE001
        raise click.ClickException(str(exc)) from exc

    for record in records:
        click.echo(f"{record['status']}\t{record['url']}\t{record['first_seen_at']}")


@state_group.command("mark")
@click.option("--url", required=True, help="URL to update.")
@click.option(
    "--status",
    type=click.Choice(["added", "skipped"]),
    required=True,
    help="New state for the article.",
)
@click.option(
    "--db-path",
    "state_db_path",
    default=_DEFAULT_DB_PATH,
    envvar="SRL_STATE_DB",
    show_default=True,
    help="Path to the state SQLite DB.",
)
def state_mark(url: str, status: str, state_db_path: str) -> None:
    """Mark a URL as added or skipped."""
    try:
        conn = state_mod.open_db(Path(state_db_path).expanduser())
        state_mod.mark_url(conn, url, status)  # type: ignore[arg-type]
        conn.close()
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise click.ClickException(str(exc)) from exc

    logger.info("Marked %s as %s", url, status)


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
    typed_transport: Literal["stdio", "sse", "streamable-http"]
    if transport == "stdio":
        typed_transport = "stdio"
    elif transport == "sse":
        typed_transport = "sse"
    else:
        typed_transport = "streamable-http"

    mcp.run(transport=typed_transport)
