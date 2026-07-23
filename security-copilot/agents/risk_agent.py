def score(findings: list[dict]) -> int:
    weights = {"critical": 40, "high": 25, "medium": 15, "low": 5}
    return min(100, sum(weights.get(str(item.get("severity", "low")).lower(), 1) for item in findings))

