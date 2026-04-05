from safari_reading_list_mcp import server


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
        }

    monkeypatch.setattr(server, "export_reading_list", fake_export)

    result = server.export_reading_list_tool(output_path="/tmp/x.json")

    assert result["success"] is True
    assert result["exported_count"] == 1
    assert "filters_applied" in result
