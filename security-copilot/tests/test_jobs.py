from app.jobs import JobManager


class FakeBackgroundTasks:
    def __init__(self):
        self.tasks = []

    def add_task(self, function, *args):
        self.tasks.append((function, args))


def test_job_manager_queues_and_runs_without_blocking_enqueue():
    background = FakeBackgroundTasks()
    manager = JobManager()
    job = manager.enqueue("scan", lambda: {"ok": True}, background)
    assert job.status == "queued"
    function, args = background.tasks[0]
    function(*args)
    assert manager.get(job.id).status == "completed"
    assert manager.get(job.id).result == {"ok": True}

