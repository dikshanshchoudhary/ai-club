from dataclasses import dataclass
from typing import Any

from tools import sigma, yara


@dataclass
class ThreatHuntingAgent:
    """Correlate hunting evidence with defensive ATT&CK context."""

    def hunt(self, query: str, evidence: list[dict[str, Any]] | None = None) -> dict:
        evidence = evidence or []
        return {
            "query": query,
            "matches": [sigma.match(query), yara.scan(query)],
            "attack_path": self.build_attack_path(evidence),
            "ioc_mapping": self.map_iocs(evidence),
            "kill_chain": self.build_kill_chain(evidence),
            "risk_score": self.risk_score(evidence),
            "status": "completed",
        }

    def build_attack_path(self, evidence: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [
            {"technique": item.get("technique", "unmapped"), "source": item.get("source", "unknown")}
            for item in evidence
        ]

    def map_iocs(self, evidence: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [
            {"ioc": item.get("ioc"), "type": item.get("ioc_type", "unknown"), "technique": item.get("technique")}
            for item in evidence
            if item.get("ioc")
        ]

    def build_kill_chain(self, evidence: list[dict[str, Any]]) -> list[str]:
        phases = {str(item.get("kill_chain_phase")) for item in evidence if item.get("kill_chain_phase")}
        return sorted(phases)

    def risk_score(self, evidence: list[dict[str, Any]]) -> int:
        score = sum(int(item.get("severity_score", 0)) for item in evidence)
        return max(0, min(100, score))


def hunt(query: str, evidence: list[dict[str, Any]] | None = None) -> dict:
    return ThreatHuntingAgent().hunt(query, evidence)
