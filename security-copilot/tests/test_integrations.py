from config.integrations import INTEGRATIONS, get_integration


def test_requested_integrations_are_registered():
    assert len(INTEGRATIONS) == 29
    assert get_integration("openai")["phase"] == "phase_1"
    assert get_integration("gitleaks")["phase"] == "phase_1"
    assert get_integration("splunk")["phase"] == "phase_3"
    assert get_integration("sentinel")["category"] == "siem"
    assert get_integration("eks")["category"] == "container"
    assert "known_exploited_vulnerabilities" in get_integration("cisa_kev")["capabilities"]
