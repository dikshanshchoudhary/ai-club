from dataclasses import dataclass
from typing import Any


SUPPORTED_SOURCES = {"apache", "windows", "linux", "firewall", "sysmon", "siem"}


@dataclass
class LogAnalysisAgent:
    """Analyze normalized security events without modifying the source system."""

    def normalize(self, source: str, events: list[dict[str, Any]]) -> dict:
        source_name = source.lower().replace(" ", "_")
        return {
            "source": source_name,
            "events": events,
            "event_count": len(events),
            "status": "ready" if source_name in SUPPORTED_SOURCES else "unsupported_source",
        }

    def detect_anomalies(self, source: str, events: list[dict[str, Any]]) -> dict:
        normalized = self.normalize(source, events)
        anomalies = [
            event for event in events
            if str(event.get("severity", "")).lower() in {"high", "critical"}
            or str(event.get("status", "")).lower() in {"failed", "denied", "blocked"}
        ]
        return {**normalized, "anomalies": anomalies, "anomaly_count": len(anomalies)}

    def explain_alert(self, alert: dict[str, Any]) -> dict:
        severity = str(alert.get("severity", "unknown")).lower()
        explanation = "The alert requires analyst review because its context is incomplete."
        if severity in {"high", "critical"}:
            explanation = "The alert is high impact and should be validated against nearby events and affected assets."
        return {"alert": alert, "explanation": explanation, "status": "review_required"}

    def find_attack_chain(self, events: list[dict[str, Any]]) -> dict:
        ordered = sorted(events, key=lambda event: str(event.get("timestamp", "")))
        return {
            "events": ordered,
            "phases": [event.get("phase", "unclassified") for event in ordered],
            "status": "correlated" if ordered else "no_events",
        }

    def root_cause_analysis(self, events: list[dict[str, Any]]) -> dict:
        failed = [event for event in events if str(event.get("status", "")).lower() in {"failed", "denied"}]
        return {
            "probable_root_cause": "repeated_failed_or_denied_activity" if failed else "insufficient_evidence",
            "supporting_events": failed,
            "confidence": "low" if not failed else "medium",
            "status": "draft",
        }


def analyze_logs(source: str, events: list[dict[str, Any]] | None = None) -> dict:
    return LogAnalysisAgent().detect_anomalies(source, events or [])
