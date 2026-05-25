from __future__ import annotations

from pathlib import Path

from config import settings
from pipeline import run_pipeline


def test_dashboard_generation(tmp_path, monkeypatch) -> None:
    output_path = tmp_path / "dashboard_test.html"
    monkeypatch.setattr(settings, "DASHBOARD_OUTPUT", str(output_path))

    result = run_pipeline()
    assert result.exists()
    content = result.read_text(encoding="utf-8")
    assert "Toyota Peru - Dashboard IDME" in content
