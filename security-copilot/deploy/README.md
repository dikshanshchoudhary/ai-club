# Deployment

Development uses `docker-compose.yml` for the frontend, backend, scanner workers, Qdrant, Postgres, and Redis. From the project root:

```powershell
cp .env.example .env
docker compose -f deploy/docker-compose.yml up --build
```

The dashboard is available at `http://localhost:3000`; the API is available at `http://localhost:8000/docs`.

The backend/worker image installs Semgrep and Checkov from PyPI and pinned Trivy `0.72.0` and Gitleaks `8.30.1` binaries during the Docker build. Scanner downloads may take several minutes on the first build.

Production uses `kubernetes/stack.yaml` as a starting point for the API, workers, ingress, Redis, Postgres, Qdrant, Prometheus, and Grafana. Replace placeholder images, create the referenced Kubernetes Secret, add persistent volumes, resource limits, TLS, network policies, and managed database credentials before production use.
