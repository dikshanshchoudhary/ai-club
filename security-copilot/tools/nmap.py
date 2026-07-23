from ._adapter import active_scans_allowed, passive_result


def scan(target: str) -> dict:
    if not active_scans_allowed():
        return {"tool": "nmap", "target": target, "status": "approval_required"}
    return passive_result("nmap", target)

