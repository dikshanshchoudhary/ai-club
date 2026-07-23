from app.dashboard.summary import build_summary


def test_dashboard_contains_phase_one_sections():
    result = build_summary({"status": "completed", "risk_score": 70}, {"threat_hunting": {"risk_score": 40}})
    assert result["risk_score"] == 70
    assert result["repository_status"] == "completed"
    assert "cloud_posture" in result
    assert "security_trends" in result

