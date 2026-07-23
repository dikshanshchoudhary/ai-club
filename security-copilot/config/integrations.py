from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Integration:
    key: str
    name: str
    category: str
    capabilities: tuple[str, ...]
    status: str = "adapter_ready"
    phase: str = "phase_2"


INTEGRATIONS = {
    item.key: item
    for item in [
        Integration("github", "GitHub API", "code", ("pull_requests", "repositories"), phase="phase_1"),
        Integration("openai", "OpenAI", "reasoning", ("analysis", "planning", "reporting", "remediation"), phase="phase_1"),
        Integration("semgrep", "Semgrep", "code", ("code_scan",), phase="phase_1"),
        Integration("trivy", "Trivy", "code", ("dependency_scan", "image_scan"), phase="phase_1"),
        Integration("gitleaks", "Gitleaks", "code", ("secret_scan",), phase="phase_1"),
        Integration("checkov", "Checkov", "code", ("iac_scan",), phase="phase_1"),
        Integration("gitlab", "GitLab API", "code", ("merge_requests", "repositories")),
        Integration("bitbucket", "Bitbucket API", "code", ("pull_requests", "repositories")),
        Integration("virustotal", "VirusTotal", "threat_intelligence", ("hash", "ip", "domain", "url")),
        Integration("abuseipdb", "AbuseIPDB", "threat_intelligence", ("ip_reputation",)),
        Integration("alienvault_otx", "AlienVault OTX", "threat_intelligence", ("ioc_search",)),
        Integration("shodan", "Shodan", "threat_intelligence", ("ip", "exposure")),
        Integration("misp", "MISP", "threat_intelligence", ("ioc_search",)),
        Integration("cisa_kev", "CISA KEV", "threat_intelligence", ("known_exploited_vulnerabilities",)),
        Integration("nvd", "NVD", "threat_intelligence", ("cve_lookup",)),
        Integration("sentinel", "Microsoft Sentinel", "siem", ("alerts", "logs", "incidents"), phase="phase_3"),
        Integration("splunk", "Splunk", "siem", ("alerts", "logs", "search"), phase="phase_3"),
        Integration("elastic", "Elastic", "siem", ("alerts", "logs", "search")),
        Integration("wazuh", "Wazuh", "siem", ("alerts", "events"), phase="phase_3"),
        Integration("qradar", "QRadar", "siem", ("offenses", "events")),
        Integration("chronicle", "Chronicle", "siem", ("detections", "search")),
        Integration("aws", "AWS", "cloud", ("iam", "posture", "cloudtrail")),
        Integration("azure", "Azure", "cloud", ("rbac", "posture", "logs"), phase="phase_3"),
        Integration("gcp", "Google Cloud", "cloud", ("iam", "posture", "logs"), phase="phase_3"),
        Integration("docker", "Docker", "container", ("image_scan", "secrets")),
        Integration("kubernetes", "Kubernetes", "container", ("cluster_scan", "workloads")),
        Integration("eks", "Amazon EKS", "container", ("cluster_scan",)),
        Integration("aks", "Azure AKS", "container", ("cluster_scan",)),
        Integration("gke", "Google GKE", "container", ("cluster_scan",)),
    ]
}


def get_integration(key: str) -> dict | None:
    integration = INTEGRATIONS.get(key.lower())
    return asdict(integration) if integration else None
