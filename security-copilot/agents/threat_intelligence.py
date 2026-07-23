from dataclasses import dataclass

from tools import abuseipdb, alienvault_otx, cve_lookup, misp, shodan, virustotal


@dataclass
class ThreatIntelligenceAgent:
    """Aggregate passive threat-intelligence lookups into a normalized response."""

    def lookup_cve(self, identifier: str) -> dict:
        return cve_lookup.lookup(identifier)

    def search_ioc(self, indicator: str) -> dict:
        return {
            "indicator": indicator,
            "sources": [
                virustotal.lookup(indicator),
                alienvault_otx.lookup(indicator),
                misp.search(indicator),
                shodan.lookup(indicator),
            ],
            "status": "completed",
        }

    def lookup_malware_hash(self, file_hash: str) -> dict:
        return {"hash": file_hash, "result": virustotal.lookup(file_hash), "status": "completed"}

    def lookup_ip_reputation(self, ip: str) -> dict:
        return {
            "ip": ip,
            "sources": [abuseipdb.lookup(ip), virustotal.lookup(ip), shodan.lookup(ip)],
            "status": "completed",
        }

    def lookup_domain_reputation(self, domain: str) -> dict:
        return {
            "domain": domain,
            "sources": [virustotal.lookup(domain), alienvault_otx.lookup(domain), misp.search(domain)],
            "status": "completed",
        }

