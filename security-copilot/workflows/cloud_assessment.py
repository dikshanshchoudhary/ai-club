from agents.cloud_security import CloudSecurityAgent


def run(provider: str, scope: str) -> dict:
    agent = CloudSecurityAgent()
    return {
        "provider": provider,
        "scope": scope,
        "iam": agent.assess_iam(provider, scope),
        "public_buckets": agent.find_public_buckets(scope),
        "open_ports": agent.find_open_ports(scope),
        "kubernetes": agent.assess_kubernetes(scope),
        "status": "completed",
    }

