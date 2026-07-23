from workflows.investigate_alert import run


def test_alert_investigation_pipeline_returns_requested_stages():
    result = run(
        "sysmon",
        [{"severity": "high", "ioc": "203.0.113.10", "technique": "T1059", "severity_score": 50}],
        {"query": "PowerShell activity"},
    )
    assert result["status"] == "completed"
    assert result["suspicious_activity"]["anomaly_count"] == 1
    assert result["mitre_mapping"][0]["technique"] == "T1059"
    assert result["ioc_enrichment"][0]["indicator"] == "203.0.113.10"
    assert result["executive_report"]["report_type"] == "executive"

