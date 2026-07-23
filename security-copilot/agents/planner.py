from dataclasses import dataclass

from agents.capabilities import CAPABILITIES
from config.approval_policy import check_action


@dataclass(frozen=True)
class SecurityPlanner:
    """Create bounded, reviewable plans from security requests."""

    def create_plan(self, request: dict) -> dict:
        objective = str(request.get("objective", "security assessment"))
        scope = request.get("scope", {})
        requested_capability = request.get("capability")
        capability = CAPABILITIES.get(str(requested_capability).lower()) if requested_capability else None
        stages = list(capability.stages) if capability else ["planner", "scanner", "analyst", "reporter"]
        return {
            "objective": objective,
            "scope": scope,
            "capability": capability.key if capability else None,
            "stages": stages,
            "steps": [
                {"id": 1, "action": "validate_scope", "requires_approval": False},
                {"id": 2, "action": "collect_passive_evidence", "requires_approval": False},
                {"id": 3, "action": "run_configured_analysis", "requires_approval": check_action("repository_scan").allowed is False},
                {"id": 4, "action": "generate_findings_and_fixes", "requires_approval": False},
            ],
            "status": "awaiting_approval",
        }
