from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Capability:
    key: str
    name: str
    category: str
    stages: tuple[str, ...]
    status: str = "planned"


CAPABILITIES = {
    item.key: item
    for item in [
        Capability("autonomous_investigation", "Autonomous investigation from a single alert", "soc", ("planner", "scanner", "analyst", "responder", "reporter")),
        Capability("pull_request_review", "Pull request security review with inline fixes", "developer", ("planner", "scanner", "analyst", "reporter")),
        Capability("secure_code_patches", "AI-generated secure code patches", "developer", ("analyst", "reviewer")),
        Capability("iac_analysis", "Infrastructure-as-Code security analysis", "cloud", ("scanner", "analyst", "reporter")),
        Capability("cloud_posture", "Cloud posture assessment", "cloud", ("scanner", "analyst", "reporter")),
        Capability("attack_path_simulation", "Attack path simulation", "threat", ("planner", "scanner", "analyst")),
        Capability("mitre_explanations", "MITRE ATT&CK mapping and explanations", "threat", ("analyst", "reporter")),
        Capability("natural_language_siem", "Natural-language SIEM queries", "soc", ("planner", "scanner", "analyst")),
        Capability("compliance_checks", "SOC 2, ISO 27001, and PCI DSS checks", "compliance", ("scanner", "analyst", "reporter")),
        Capability("executive_dashboards", "Executive dashboards with risk trends", "reporting", ("analyst", "reporter", "dashboard")),
        Capability("security_memory", "Previous incidents and recurring vulnerabilities", "platform", ("memory", "analyst")),
        Capability("multi_agent_collaboration", "Planner-to-reporter multi-agent collaboration", "platform", ("planner", "scanner", "analyst", "responder", "reporter")),
    ]
}


def describe_capability(key: str) -> dict | None:
    capability = CAPABILITIES.get(key.lower())
    return asdict(capability) if capability else None

