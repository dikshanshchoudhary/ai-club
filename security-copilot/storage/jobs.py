import json


class PostgresJobStore:
    def __init__(self, database_url: str):
        self.database_url = database_url

    def _connect(self):
        try:
            import psycopg
            from psycopg.rows import dict_row
        except ImportError as exc:
            raise RuntimeError("Install psycopg[binary] to enable PostgreSQL job persistence") from exc
        return psycopg.connect(self.database_url, row_factory=dict_row)

    def update(self, external_id: str, status: str, progress: int, stage: str, *, result: dict | None = None, error: str | None = None) -> None:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO jobs (external_id, name, status, progress, stage, result, error) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (external_id) DO UPDATE SET status = EXCLUDED.status, progress = EXCLUDED.progress, stage = EXCLUDED.stage, result = EXCLUDED.result, error = EXCLUDED.error, updated_at = now()", (external_id, "live_repository_scan", status, progress, stage, json.dumps(result) if result else None, error))

    def get(self, external_id: str) -> dict | None:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT external_id, name, status, progress, stage, result, error, created_at, updated_at FROM jobs WHERE external_id = %s", (external_id,))
                return cursor.fetchone()

