from click.testing import CliRunner

from safari_reading_list_mcp import cli


def test_cli_export_week_invokes_service(monkeypatch) -> None:
    captured: dict[str, object] = {}

    def fake_export_reading_list(**kwargs):
        captured.update(kwargs)
        return {
            "success": True,
            "output_path": kwargs["output_path"],
            "exported_count": 2,
            "total_count": 5,
            "filters_applied": {"default_range": True},
            "warnings": [],
        }

    monkeypatch.setattr(cli, "export_reading_list", fake_export_reading_list)

    runner = CliRunner()
    result = runner.invoke(cli.main, ["export", "week", "--output", "week.json"])

    assert result.exit_code == 0
    assert result.output == ""
    assert captured["output_path"] == "week.json"
    assert captured.get("full_export") is None


def test_cli_export_all_invokes_full_export(monkeypatch) -> None:
    captured: dict[str, object] = {}

    def fake_export_reading_list(**kwargs):
        captured.update(kwargs)
        return {
            "success": True,
            "output_path": kwargs["output_path"],
            "exported_count": 5,
            "total_count": 5,
            "filters_applied": {"full_export": True},
            "warnings": [],
        }

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
        return {
            "success": True,
            "output_path": kwargs["output_path"],
            "exported_count": 1,
            "total_count": 5,
            "filters_applied": {
                "start_time": kwargs["start_time"],
                "end_time": kwargs["end_time"],
            },
            "warnings": [],
        }

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
            "success": True,
            "output_path": kwargs["output_path"],
            "exported_count": 1,
            "total_count": 2,
            "filters_applied": {"default_range": True},
            "warnings": ["missing timestamp on one entry"],
        }

    monkeypatch.setattr(cli, "export_reading_list", fake_export_reading_list)

    runner = CliRunner()
    result = runner.invoke(cli.main, ["export", "week", "--output", "week.json"])

    assert result.exit_code == 0
    assert "missing timestamp on one entry" in result.output


def test_cli_supports_debug_log_level(monkeypatch) -> None:
    def fake_export_reading_list(**kwargs):
        return {
            "success": True,
            "output_path": kwargs["output_path"],
            "exported_count": 1,
            "total_count": 1,
            "filters_applied": {"default_range": True},
            "warnings": [],
        }

    monkeypatch.setattr(cli, "export_reading_list", fake_export_reading_list)

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
