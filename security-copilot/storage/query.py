class PostgresQueryStore:
    """Read-only dashboard query layer backed by the PostgreSQL schema."""

    def __init__(self, database_url: str):
        self.database_url = database_url

    def _connect(self):
        try:
            import psycopg
            from psycopg.rows import dict_row
        except ImportError as exc:
            raise RuntimeError("Install psycopg[binary] to enable PostgreSQL reads") from exc
        return psycopg.connect(self.database_url, row_factory=dict_row)

    def dashboard(self) -> dict:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT COALESCE(MAX(risk_score), 0) AS risk_score FROM repository_scans")
                risk_score = cursor.fetchone()["risk_score"]
                cursor.execute("SELECT COUNT(*) AS total FROM findings WHERE status = 'open'")
                total_findings = cursor.fetchone()["total"]
                cursor.execute("SELECT COUNT(*) AS total FROM findings WHERE status = 'open' AND severity = 'critical'")
                critical_findings = cursor.fetchone()["total"]
                cursor.execute("SELECT COUNT(*) AS total FROM repositories")
                repositories = cursor.fetchone()["total"]
                cursor.execute("SELECT COUNT(*) AS total FROM repository_scans WHERE status = 'completed'")
                completed_scans = cursor.fetchone()["total"]
        return {"risk_score": risk_score, "total_findings": total_findings, "critical_findings": critical_findings, "repositories": repositories, "completed_scans": completed_scans, "data_source": "postgresql"}

    def findings(self, limit: int = 100) -> list[dict]:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, tool, rule_id, severity, title, description, file_path, line_number, evidence, status, created_at FROM findings ORDER BY created_at DESC LIMIT %s", (limit,))
                return cursor.fetchall()

    def repositories(self) -> list[dict]:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, provider, external_id, name, url, default_branch, created_at FROM repositories ORDER BY created_at DESC")
                return cursor.fetchall()

    def finding(self, finding_id: str) -> dict | None:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, tool, rule_id, severity, title, description, file_path, line_number, evidence, status, created_at FROM findings WHERE id = %s", (finding_id,))
                return cursor.fetchone()
