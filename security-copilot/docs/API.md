# API reference

The FastAPI service runs on port `8000`. Interactive OpenAPI documentation is available at `/docs`.

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Service health |
| POST | `/plan` | Create an approval-aware plan |
| POST | `/jobs/live-repository-scan` | Queue a real repository scan |
| GET | `/jobs/{job_id}` | Poll job status |
| GET | `/mvp/dashboard/live` | Read dashboard metrics from PostgreSQL |
| GET | `/mvp/findings` | Read stored findings from PostgreSQL |
| POST | `/mvp/chat` | Ask a RAG-grounded question |
| POST | `/mvp/reports/pdf` | Download a PDF report |
| POST | `/mvp/alerts/investigate` | Investigate normalized alert events |
| POST | `/mvp/cloud/assess` | Run cloud assessment boundary |

Example:

```json
POST /jobs/live-repository-scan
{"source":"demo/vulnerable-repo"}
```

