import os

from celery import Celery

from workflows.live_repository_scan import run_and_store


celery_app = Celery(
    "security_copilot",
    broker=os.getenv("REDIS_URL", "redis://redis:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", os.getenv("REDIS_URL", "redis://redis:6379/1")),
)
celery_app.conf.update(task_track_started=True, result_expires=86400, task_serializer="json", accept_content=["json"], result_serializer="json")


@celery_app.task(bind=True, name="security_copilot.scan_repository")
def scan_repository_task(self, source: str, database_url: str | None = None, repository_id: str | None = None) -> dict:
    job_store = None
    if database_url:
        from storage.jobs import PostgresJobStore
        job_store = PostgresJobStore(database_url)
        job_store.update(self.request.id, "running", 10, "clone_repository")
    try:
        if job_store:
            job_store.update(self.request.id, "running", 25, "run_scanners")
        result = run_and_store(source, database_url, repository_id)
        if job_store:
            job_store.update(self.request.id, "completed", 100, "stored_results", result=result)
        return result
    except Exception as exc:
        if job_store:
            job_store.update(self.request.id, "failed", 100, "failed", error=str(exc))
        raise

