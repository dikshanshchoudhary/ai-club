# Secure deployment checklist

- Put the application behind the provided Nginx reverse proxy or a managed HTTPS load balancer.
- Replace `example.com` and mount certificates at `/etc/nginx/tls`.
- Keep PostgreSQL and Qdrant private; expose only the frontend and proxy.
- Use persistent encrypted volumes for PostgreSQL and Qdrant.
- Run scheduled PostgreSQL backups with `deploy/postgres/backup.ps1` or an equivalent managed backup service, and test restores.
- Apply firewall rules that allow only HTTPS publicly and internal service traffic privately.
- Keep API rate limiting enabled at the proxy and add authenticated per-user limits before production.
- Keep destructive actions blocked by `config/approval_policy.py`; require audited human approval for state-changing actions.
- Use managed secrets instead of `.env` in production.
- Add TLS termination, security headers, monitoring, and alerting before public launch.

