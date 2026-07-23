from agents.threat_hunting import ThreatHuntingAgent


def test_hunt_returns_required_outputs():
    result = ThreatHuntingAgent().hunt(
        "suspicious PowerShell",
        [{
            "technique": "T1059.001",
            "source": "sysmon",
            "ioc": "203.0.113.10",
            "ioc_type": "ip",
            "kill_chain_phase": "execution",
            "severity_score": 80,
        }],
    )
    assert result["risk_score"] == 80
    assert result["attack_path"][0]["technique"] == "T1059.001"
    assert result["ioc_mapping"][0]["type"] == "ip"
    assert result["kill_chain"] == ["execution"]

