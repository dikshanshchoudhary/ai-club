# Troubleshooting

### Dashboard says `DATABASE_URL is required`

Set `DATABASE_URL` in `.env`, restart Compose, and apply `deploy/postgres/001_initial_schema.sql`.

### Scanner is unavailable

Rebuild the worker image with `docker compose -f deploy/docker-compose.yml build --no-cache scanner-workers`. The image installs Semgrep, Checkov, Trivy, and Gitleaks during build; inspect worker logs if a scanner exits non-zero.

### Frontend cannot reach the API

Confirm ports `3000` and `8000`, and set `NEXT_PUBLIC_API_URL` if the API is not local.

### Model responses show `not_configured`

Set `OPENAI_API_KEY` in `.env`. The application reports an unconfigured state instead of fabricating analysis.
