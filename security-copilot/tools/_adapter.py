import os


def active_scans_allowed() -> bool:
    return os.getenv("SECURITY_COPILOT_ALLOW_ACTIVE_SCANS", "false").lower() == "true"


def passive_result(tool: str, target: str) -> dict:
    return {"tool": tool, "target": target, "status": "not_configured", "findings": []}

