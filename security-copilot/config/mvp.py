MVP_PHASE = "phase_1"

MVP_CAPABILITIES = {
    "repository_security": {
        "features": ["ai_code_review", "secret_detection", "dependency_scanning", "docker_scanning", "iac_scanning", "pull_request_review", "risk_scoring", "remediation_suggestions"],
        "integrations": ["github", "gitlab", "bitbucket"],
        "scanners": ["semgrep", "codeql", "trivy", "gitleaks", "checkov", "tfsec", "grype"],
    },
    "alert_investigation": {
        "inputs": ["syslog", "sysmon", "windows_event", "linux", "aws_cloudtrail", "azure", "gcp", "edr", "siem"],
        "outputs": ["explanation", "severity", "attack_chain", "mitre_mapping", "ioc_enrichment", "remediation", "summary"],
    },
    "cloud_security": {
        "providers": ["aws", "azure", "gcp"],
        "checks": ["iam", "public_buckets", "security_groups", "open_ports", "kubernetes", "containers", "secrets", "misconfigurations", "compliance"],
        "tools": ["prowler", "scoutsuite", "trivy", "kube-bench", "kube-hunter"],
    },
    "executive_dashboard": {
        "sections": ["risk_score", "critical_findings", "repository_status", "cloud_posture", "recent_incidents", "compliance", "security_trends", "ai_recommendations"],
    },
}

