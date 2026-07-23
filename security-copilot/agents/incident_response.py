from dataclasses import dataclass
from typing import Any


@dataclass
class IncidentResponseAgent:
    """Produce reviewable response guidance; execution remains human-approved."""

    def generate_response_plan(self, incident: dict[str, Any]) -> dict:
        return {
            "incident": incident,
            "phases": [
                {"name": "triage", "actions": ["validate alert", "identify affected assets"]},
                {"name": "containment", "actions": self.recommend_containment(incident)},
                {"name": "eradication", "actions": self.recommend_eradication(incident)},
                {"name": "recovery", "actions": self.recovery_steps(incident)},
            ],
            "requires_approval": True,
            "status": "plan_ready",
        }

    def recommend_containment(self, incident: dict[str, Any]) -> list[str]:
        actions = ["Preserve logs and forensic evidence", "Restrict affected identities and network paths"]
        if incident.get("ransomware"):
            actions.insert(0, "Isolate suspected hosts from the network")
        return actions

    def recommend_eradication(self, incident: dict[str, Any]) -> list[str]:
        return [
            "Remove persistence and malicious artifacts",
            "Rotate exposed credentials and revoke active sessions",
            "Patch the exploited weakness and validate the fix",
        ]

    def recovery_steps(self, incident: dict[str, Any]) -> list[str]:
        return [
            "Restore from a verified clean backup when required",
            "Monitor affected assets for recurrence",
            "Document lessons learned and close follow-up actions",
        ]

    def generate_timeline(self, events: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return sorted(events, key=lambda event: str(event.get("timestamp", "")))


def recommend_response(alert: dict) -> dict:
    return IncidentResponseAgent().generate_response_plan(alert)
