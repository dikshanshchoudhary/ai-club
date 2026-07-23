from dataclasses import dataclass

from tools import kube_bench, kube_hunter, prowler, scoutsuite


@dataclass
class CloudSecurityAgent:
    """Coordinate cloud posture checks; adapters are read-only until configured."""

    def assess_iam(self, provider: str, scope: str) -> dict:
        provider = provider.lower()
        if provider == "aws":
            return prowler.check(scope, check_type="iam")
        if provider in {"azure", "gcp"}:
            return scoutsuite.check(scope, provider=provider, check_type="iam")
        return {"provider": provider, "scope": scope, "status": "unsupported_provider"}

    def find_public_buckets(self, scope: str) -> dict:
        return scoutsuite.check(scope, provider="aws", check_type="public_storage")

    def find_open_ports(self, scope: str) -> dict:
        return prowler.check(scope, check_type="network_exposure")

    def assess_kubernetes(self, cluster: str) -> dict:
        return {
            "cluster": cluster,
            "checks": [kube_bench.check(cluster), kube_hunter.check(cluster)],
            "status": "completed",
        }


def assess_cloud(account: str) -> dict:
    return CloudSecurityAgent().assess_iam("aws", account)
