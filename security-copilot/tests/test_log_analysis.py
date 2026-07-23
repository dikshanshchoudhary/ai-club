from agents.log_analysis import LogAnalysisAgent


def test_detects_high_severity_and_denied_events():
    result = LogAnalysisAgent().detect_anomalies(
        "Firewall Logs",
        [{"status": "denied"}, {"severity": "high"}, {"status": "allowed"}],
    )
    assert result["source"] == "firewall_logs"
    assert result["anomaly_count"] == 2


def test_attack_chain_is_timestamp_ordered():
    result = LogAnalysisAgent().find_attack_chain([
        {"timestamp": "2026-01-02", "phase": "impact"},
        {"timestamp": "2026-01-01", "phase": "initial_access"},
    ])
    assert result["phases"] == ["initial_access", "impact"]

