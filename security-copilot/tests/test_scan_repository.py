from workflows.scan_repository import run


def test_repository_scan_pipeline_returns_requested_stages():
    result = run(".")
    assert result["status"] == "completed"
    assert result["semgrep_scan"]["tool"] == "semgrep"
    assert result["trivy_scan"]["tool"] == "trivy"
    assert "ai_analysis" in result
    assert 0 <= result["risk_score"] <= 100
    assert result["report"]["status"] == "draft"

