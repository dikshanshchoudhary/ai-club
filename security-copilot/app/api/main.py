from fastapi import BackgroundTasks, FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

from agents.planner import SecurityPlanner
from app.dashboard.summary import build_summary
from workflows.cloud_assessment import run as run_cloud_assessment
from workflows.investigate_alert import run as run_investigation
from workflows.scan_repository import run as run_repository_scan
from workflows.live_repository_scan import run_and_store as run_live_repository_scan
from app.jobs import job_manager
from agents.chat_agent import AIChatAgent
from memory.retriever import InMemoryRetriever
from config.settings import settings
from storage.query import PostgresQueryStore
from workers.celery_app import scan_repository_task

app = FastAPI(title="Security Copilot", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_methods=["*"], allow_headers=["*"])
planner = SecurityPlanner()
chat_retriever = InMemoryRetriever()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "security-copilot"}


@app.post("/plan")
def plan(request: dict) -> dict:
    return planner.create_plan(request)


@app.post("/mvp/repository/scan")
def repository_scan(request: dict) -> dict:
    return run_repository_scan(request["path"], request.get("report_type", "technical"), request.get("output_format", "markdown"))


@app.post("/mvp/alerts/investigate")
def investigate_alert(request: dict) -> dict:
    return run_investigation(request["source"], request.get("events", []), request.get("alert"))


@app.post("/mvp/cloud/assess")
def cloud_assess(request: dict) -> dict:
    return run_cloud_assessment(request["provider"], request["scope"])


@app.post("/mvp/dashboard")
def dashboard(request: dict) -> dict:
    return build_summary(request.get("repository_scan"), request.get("investigation"), request.get("cloud_assessment"))


@app.post("/jobs/repository-scan")
def queue_repository_scan(request: dict, background_tasks: BackgroundTasks) -> dict:
    job = job_manager.enqueue("repository_scan", lambda: run_repository_scan(request["path"]), background_tasks)
    return {"job_id": job.id, "status": job.status}


@app.post("/jobs/live-repository-scan")
def queue_live_repository_scan(request: dict, background_tasks: BackgroundTasks) -> dict:
    task = scan_repository_task.delay(request["source"], settings.database_url, request.get("repository_id"))
    return {"job_id": task.id, "status": "queued", "backend": "celery"}


@app.get("/jobs/{job_id}")
def get_job(job_id: str) -> dict:
    if settings.database_url:
        from storage.jobs import PostgresJobStore
        stored = PostgresJobStore(settings.database_url).get(job_id)
        if stored:
            return stored
    async_result = scan_repository_task.AsyncResult(job_id)
    if async_result.state != "PENDING":
        return {"job_id": job_id, "name": "live_repository_scan", "status": async_result.state.lower(), "result": async_result.result if async_result.successful() else None, "error": str(async_result.result) if async_result.failed() else None}
    job = job_manager.get(job_id)
    if job is None:
        return {"job_id": job_id, "status": "not_found"}
    return {"job_id": job.id, "name": job.name, "status": job.status, "result": job.result, "error": job.error}


@app.post("/mvp/chat")
def chat(request: dict) -> dict:
    return AIChatAgent(chat_retriever).ask(request["question"])


@app.get("/mvp/dashboard/live")
def live_dashboard() -> dict:
    if not settings.database_url:
        return {"status": "not_configured", "data_source": "postgresql", "message": "DATABASE_URL is required"}
    return {"status": "completed", "dashboard": PostgresQueryStore(settings.database_url).dashboard()}


@app.get("/mvp/findings")
def live_findings(limit: int = 100) -> dict:
    if not settings.database_url:
        return {"status": "not_configured", "data_source": "postgresql", "findings": [], "message": "DATABASE_URL is required"}
    return {"status": "completed", "data_source": "postgresql", "findings": PostgresQueryStore(settings.database_url).findings(limit)}


@app.get("/mvp/repositories")
def live_repositories() -> dict:
    if not settings.database_url:
        return {"status": "not_configured", "data_source": "postgresql", "repositories": [], "message": "DATABASE_URL is required"}
    return {"status": "completed", "data_source": "postgresql", "repositories": PostgresQueryStore(settings.database_url).repositories()}


@app.get("/mvp/findings/{finding_id}")
def finding_detail(finding_id: str) -> dict:
    if not settings.database_url:
        return {"status": "not_configured", "data_source": "postgresql", "finding": None, "message": "DATABASE_URL is required"}
    return {"status": "completed", "data_source": "postgresql", "finding": PostgresQueryStore(settings.database_url).finding(finding_id)}


@app.post("/mvp/reports")
def generate_report(request: dict) -> dict:
    from agents.report_generator import SecurityReportAgent
    return SecurityReportAgent().create(request.get("findings", []), request.get("report_type", "technical"), request.get("output_format", "markdown"))


@app.post("/mvp/reports/pdf")
def report_pdf(request: dict) -> Response:
    from agents.report_generator import SecurityReportAgent
    pdf = SecurityReportAgent().render_pdf(request.get("findings", []), request.get("report_type", "technical"))
    return Response(content=pdf, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=security-report.pdf"})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.api.main:app", host="127.0.0.1", port=8000, reload=False)
