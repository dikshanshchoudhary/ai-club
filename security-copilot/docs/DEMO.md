# Beta demo guide

## Start

```powershell
cp .env.example .env
docker compose -f deploy/docker-compose.yml up --build
```

Open **Repositories**, use `demo/vulnerable-repo`, and click **Scan**. The UI polls the background job until completion. Review **Findings**, inspect **Dashboard**, then use **Reports** to download a PDF.

The demo files are intentionally insecure and contain fake, clearly marked values. Never deploy them.

