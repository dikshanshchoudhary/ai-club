# AI Security Copilot

An AI-assisted security operations workspace for repository scanning, alert investigation, cloud assessment, and executive reporting.

## Beta capabilities

- Live Semgrep, Trivy, Gitleaks, and Checkov repository scans
- PostgreSQL-backed findings and dashboard metrics
- RAG-grounded AI chat over scan evidence
- Executive and technical reports with PDF, Markdown, and JSON output
- Background scan jobs with status polling
- Read-only-by-default approval policy
- Docker Compose development environment

## Quick start

```powershell
git clone <repository-url>
cd security-copilot
cp .env.example .env
docker compose -f deploy/docker-compose.yml up --build
```

Open http://localhost:3000 for the dashboard or http://localhost:8000/docs for API documentation.

## Local demo

Use the intentionally vulnerable examples in [demo](demo). Start a scan with the Repositories page or:

```powershell
security scan demo/vulnerable-repo
```

See [docs/DEMO.md](docs/DEMO.md) for the complete walkthrough.

## Documentation

- [Architecture](ARCHITECTURE.md)
- [API reference](docs/API.md)
- [Demo guide](docs/DEMO.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [Deployment](deploy/README.md)
- [Secure deployment checklist](docs/SECURE_DEPLOYMENT.md)
- [Post-MVP roadmap](ROADMAP.md)

## Security model

Never hardcode credentials. Copy `.env.example` to `.env` for local development and use AWS Secrets Manager, Azure Key Vault, Google Secret Manager, or HashiCorp Vault in production. Scans and lookups are read-only by default. State-changing actions require approval; dangerous operations are blocked by default.

## Status

This is a beta scaffold becoming an MVP. External scanner binaries, PostgreSQL, and model credentials must be configured for live results.
