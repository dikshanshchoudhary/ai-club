import json


class PostgresFindingStore:
    """Optional PostgreSQL sink. Install psycopg and configure DATABASE_URL to enable it."""

    def __init__(self, database_url: str):
        self.database_url = database_url

    def save_scan(self, repository_id: str, scan: dict) -> None:
        try:
            import psycopg
        except ImportError as exc:
            raise RuntimeError("Install psycopg[binary] to enable PostgreSQL persistence") from exc
        with psycopg.connect(self.database_url) as connection:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO repository_scans (repository_id, status, risk_score) VALUES (%s, %s, %s) RETURNING id", (repository_id, scan.get("status", "completed"), scan.get("risk_score")))
                scan_id = cursor.fetchone()[0]
                for finding in scan.get("findings", []):
                    cursor.execute("INSERT INTO findings (scan_id, tool, rule_id, severity, title, file_path, line_number, evidence) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (scan_id, finding.get("tool", "unknown"), finding.get("rule_id"), finding.get("severity", "unknown"), finding.get("title", "Security finding"), finding.get("file"), finding.get("line"), json.dumps(finding.get("raw", {}))))

