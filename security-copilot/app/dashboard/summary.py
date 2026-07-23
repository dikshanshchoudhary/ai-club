def build_summary(repository_scan: dict | None = None, investigation: dict | None = None, cloud_assessment: dict | None = None) -> dict:
    repository_scan = repository_scan or {}
    investigation = investigation or {}
    cloud_assessment = cloud_assessment or {}
    risk_values = [repository_scan.get("risk_score", 0), investigation.get("threat_hunting", {}).get("risk_score", 0)]
    return {
        "risk_score": min(100, max(risk_values, default=0)),
        "critical_findings": [finding for finding in repository_scan.get("ai_analysis", {}).get("findings", []) if finding.get("severity") == "critical"],
        "repository_status": repository_scan.get("status", "not_run"),
        "cloud_posture": cloud_assessment.get("status", "not_run"),
        "recent_incidents": 1 if investigation else 0,
        "compliance": "review_required",
        "security_trends": [],
        "ai_recommendations": repository_scan.get("fix_suggestions", []) + investigation.get("remediation_steps", []),
    }

