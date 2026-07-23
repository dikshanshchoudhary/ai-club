import uuid
from dataclasses import dataclass, field
from threading import Lock
from typing import Any, Callable


@dataclass
class Job:
    id: str
    name: str
    status: str = "queued"
    result: Any = None
    error: str | None = None


@dataclass
class JobManager:
    jobs: dict[str, Job] = field(default_factory=dict)
    lock: Lock = field(default_factory=Lock)

    def enqueue(self, name: str, task: Callable[[], Any], background_tasks: Any) -> Job:
        job = Job(id=str(uuid.uuid4()), name=name)
        with self.lock:
            self.jobs[job.id] = job
        background_tasks.add_task(self._run, job.id, task)
        return job

    def get(self, job_id: str) -> Job | None:
        return self.jobs.get(job_id)

    def _run(self, job_id: str, task: Callable[[], Any]) -> None:
        job = self.jobs[job_id]
        job.status = "running"
        try:
            job.result = task()
            job.status = "completed"
        except Exception as exc:
            job.error = str(exc)
            job.status = "failed"


job_manager = JobManager()

