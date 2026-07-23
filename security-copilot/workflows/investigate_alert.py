from agents.incident_response import IncidentResponseAgent
from agents.log_analysis import LogAnalysisAgent
from agents.report_generator import SecurityReportAgent
from agents.threat_hunting import ThreatHuntingAgent
from agents.threat_intelligence import ThreatIntelligenceAgent


def run(source: str, events: list[dict], alert: dict | None = None) -> dict:
    """Correlate uploaded logs into a reviewable incident investigation."""
    log_agent = LogAnalysisAgent()
    hunting_agent = ThreatHuntingAgent()
    intel_agent = ThreatIntelligenceAgent()
    response_agent = IncidentResponseAgent()

    suspicious = log_agent.detect_anomalies(source, events)
    hunt = hunting_agent.hunt(alert.get("query", "suspicious activity") if alert else "suspicious activity", events)
    iocs = [event.get("ioc") for event in events if event.get("ioc")]
    enrichment = [intel_agent.search_ioc(ioc) for ioc in iocs]
    incident = alert or {"source": source, "anomaly_count": suspicious["anomaly_count"]}
    response_plan = response_agent.generate_response_plan(incident)
    remediation = response_agent.recovery_steps(incident) + response_agent.recommend_eradication(incident)
    report = SecurityReportAgent().create(
        [{"source": source, "anomalies": suspicious["anomalies"], "risk_score": hunt["risk_score"]}],
        report_type="executive",
        output_format="markdown",
    )
    return {
        "suspicious_activity": suspicious,
        "threat_hunting": hunt,
        "mitre_mapping": hunt["attack_path"],
        "ioc_enrichment": enrichment,
        "incident_response": response_plan,
        "remediation_steps": remediation,
        "executive_report": report,
        "status": "completed",
    }
