from pathlib import Path

import pytest
from click.testing import CliRunner

from safari_reading_list_mcp import cli
from safari_reading_list_mcp import state


def _fake_export(**kwargs):
    return {
        "success": True,
        "output_path": kwargs["output_path"],
        "exported_count": 2,
        "total_count": 5,
        "filters_applied": {"default_range": True},
        "warnings": [],
        "new_to_db": 0,
        "already_added": 0,
        "already_skipped": 0,
    }


def test_cli_export_week_invokes_service(monkeypatch) -> None:
    captured: dict[str, object] = {}

    def fake_export_reading_list(**kwargs):
        captured.update(kwargs)
        return _fake_export(**kwargs)

    monkeypatch.setattr(cli, "export_reading_list", fake_export_reading_list)

    runner = CliRunner()
    result = runner.invoke(cli.main, ["export", "week", "--output", "week.json"])

    assert result.exit_code == 0
    assert result.output == ""
    assert captured["output_path"] == "week.json"
    assert captured.get("full_export") is False


def test_cli_export_all_invokes_full_export(monkeypatch) -> None:
    captured: dict[str, object] = {}

    def fake_export_reading_list(**kwargs):
        captured.update(kwargs)
        return _fake_export(**kwargs)

    monkeypatch.setattr(cli, "export_reading_list", fake_export_reading_list)

    runner = CliRunner()
    result = runner.invoke(cli.main, ["export", "all", "--output", "all.json"])

    assert result.exit_code == 0
    assert result.output == ""
    assert captured["full_export"] is True


def test_cli_export_range_passes_start_and_end(monkeypatch) -> None:
    captured: dict[str, object] = {}

    def fake_export_reading_list(**kwargs):
        captured.update(kwargs)
        return _fake_export(**kwargs)

    monkeypatch.setattr(cli, "export_reading_list", fake_export_reading_list)

    runner = CliRunner()
    result = runner.invoke(
        cli.main,
        [
            "export",
            "range",
            "--start",
            "2026-03-01T00:00:00Z",
            "--end",
            "2026-03-31T23:59:59Z",
            "--output",
            "range.json",
        ],
    )

    assert result.exit_code == 0
    assert result.output == ""
    assert captured["start_time"] == "2026-03-01T00:00:00Z"
    assert captured["end_time"] == "2026-03-31T23:59:59Z"


def test_cli_logs_warnings_to_stderr(monkeypatch) -> None:
    def fake_export_reading_list(**kwargs):
        return {
            **_fake_export(**kwargs),
            "warnings": ["missing timestamp on one entry"],
        }

    monkeypatch.setattr(cli, "export_reading_list", fake_export_reading_list)

    runner = CliRunner()
    result = runner.invoke(cli.main, ["export", "week", "--output", "week.json"])

    assert result.exit_code == 0
    assert "missing timestamp on one entry" in result.output


def test_cli_supports_debug_log_level(monkeypatch) -> None:
    monkeypatch.setattr(cli, "export_reading_list", _fake_export)

    runner = CliRunner()
    result = runner.invoke(
        cli.main,
        ["--log-level", "DEBUG", "export", "week", "--output", "week.json"],
    )

    assert result.exit_code == 0
    assert "exported_count" in result.output


def test_cli_serve_passes_transport(monkeypatch) -> None:
    calls: list[str] = []

    class FakeMCP:
        def run(self, *, transport: str) -> None:
            calls.append(transport)

    monkeypatch.setattr(cli, "mcp", FakeMCP())

    runner = CliRunner()
    result = runner.invoke(cli.main, ["serve", "--transport", "stdio"])

    assert result.exit_code == 0
    assert calls == ["stdio"]


@pytest.mark.req("state-tracking.CLI.1")
def test_cli_export_week_passes_unprocessed_only_flag(monkeypatch) -> None:
    captured: dict[str, object] = {}

    def fake_export_reading_list(**kwargs):
        captured.update(kwargs)
        return _fake_export(**kwargs)

    monkeypatch.setattr(cli, "export_reading_list", fake_export_reading_list)

    runner = CliRunner()
    result = runner.invoke(
        cli.main,
        ["export", "week", "--output", "week.json", "--unprocessed-only"],
    )

    assert result.exit_code == 0
    assert captured.get("unprocessed_only") is True


@pytest.mark.req("state-tracking.CLI.2")
def test_cli_export_week_passes_db_path(monkeypatch) -> None:
    captured: dict[str, object] = {}

    def fake_export_reading_list(**kwargs):
        captured.update(kwargs)
        return _fake_export(**kwargs)

    monkeypatch.setattr(cli, "export_reading_list", fake_export_reading_list)

    runner = CliRunner()
    result = runner.invoke(
        cli.main,
        ["export", "week", "--output", "week.json", "--db-path", "/tmp/test.db"],
    )

    assert result.exit_code == 0
    assert captured.get("state_db_path") == "/tmp/test.db"


@pytest.mark.req("state-tracking.CLI.3")
def test_cli_state_stats_shows_counts(tmp_path: Path) -> None:
    db_path = tmp_path / "state.db"
    conn = state.open_db(db_path)
    state.upsert_pending(conn, ["https://a.com", "https://b.com", "https://c.com"])
    state.mark_url(conn, "https://a.com", "added")
    state.mark_url(conn, "https://b.com", "skipped")
    conn.close()

    runner = CliRunner()
    result = runner.invoke(cli.main, ["state", "stats", "--db-path", str(db_path)])

    assert result.exit_code == 0
    assert "pending" in result.output
    assert "1" in result.output  # added count
    assert "skipped" in result.output


@pytest.mark.req("state-tracking.CLI.4")
def test_cli_state_list_filters_by_status(tmp_path: Path) -> None:
    db_path = tmp_path / "state.db"
    conn = state.open_db(db_path)
    state.upsert_pending(conn, ["https://pending.com", "https://other.com"])
    state.mark_url(conn, "https://other.com", "added")
    conn.close()

    runner = CliRunner()
    result = runner.invoke(
        cli.main, ["state", "list", "--status", "pending", "--db-path", str(db_path)]
    )

    assert result.exit_code == 0
    assert "https://pending.com" in result.output
    assert "https://other.com" not in result.output


@pytest.mark.req("state-tracking.CLI.5")
def test_cli_state_mark_transitions_url(tmp_path: Path) -> None:
    db_path = tmp_path / "state.db"
    conn = state.open_db(db_path)
    state.upsert_pending(conn, ["https://x.com"])
    conn.close()

    runner = CliRunner()
    result = runner.invoke(
        cli.main,
        ["state", "mark", "--url", "https://x.com", "--status", "added", "--db-path", str(db_path)],
    )

    assert result.exit_code == 0

    conn = state.open_db(db_path)
    records = state.get_by_status(conn, "added")
    conn.close()
    assert len(records) == 1
    assert records[0]["url"] == "https://x.com"


@pytest.mark.req("state-tracking.CLI.6")
def test_cli_state_mark_unknown_url_exits_nonzero(tmp_path: Path) -> None:
    db_path = tmp_path / "state.db"
    state.open_db(db_path).close()

    runner = CliRunner()
    result = runner.invoke(
        cli.main,
        ["state", "mark", "--url", "https://ghost.com", "--status", "skipped", "--db-path", str(db_path)],
    )

    assert result.exit_code != 0
