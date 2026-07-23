from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class KnowledgeSource:
    key: str
    name: str
    category: str
    purpose: str
    local_path: str


KNOWLEDGE_SOURCES = {
    source.key: source
    for source in [
        KnowledgeSource("mitre_attack", "MITRE ATT&CK", "threat", "Adversary tactics, techniques, and procedures", "knowledge/MITRE"),
        KnowledgeSource("owasp_top_10", "OWASP Top 10", "application", "Common web application security risks", "knowledge/OWASP"),
        KnowledgeSource("cwe", "CWE", "weakness", "Common software and hardware weakness taxonomy", "knowledge/CWE"),
        KnowledgeSource("capec", "CAPEC", "attack_pattern", "Common attack pattern catalog", "knowledge/CAPEC"),
        KnowledgeSource("cve", "CVE", "vulnerability", "Public vulnerability identifiers", "knowledge/CVE"),
        KnowledgeSource("cisa_kev", "CISA KEV", "vulnerability", "Known exploited vulnerabilities", "knowledge/CISA_KEV"),
        KnowledgeSource("nist", "NIST", "governance", "Cybersecurity frameworks and guidance", "knowledge/NIST"),
        KnowledgeSource("pci_dss", "PCI DSS", "compliance", "Payment card security requirements", "knowledge/PCI_DSS"),
        KnowledgeSource("soc2", "SOC 2", "compliance", "Trust services criteria for service organizations", "knowledge/SOC2"),
        KnowledgeSource("iso27001", "ISO 27001", "compliance", "Information security management system controls", "knowledge/ISO27001"),
    ]
}


def get_source(key: str) -> dict | None:
    source = KNOWLEDGE_SOURCES.get(key.lower())
    return asdict(source) if source else None

