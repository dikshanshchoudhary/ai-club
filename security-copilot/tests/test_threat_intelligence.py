from agents.threat_intelligence import ThreatIntelligenceAgent


def test_ioc_search_uses_all_configured_sources():
    result = ThreatIntelligenceAgent().search_ioc("203.0.113.10")
    assert {source["tool"] for source in result["sources"]} == {"virustotal", "alienvault_otx", "misp", "shodan"}


def test_ip_reputation_uses_reputation_sources():
    result = ThreatIntelligenceAgent().lookup_ip_reputation("203.0.113.10")
    assert {source["tool"] for source in result["sources"]} == {"abuseipdb", "virustotal", "shodan"}

