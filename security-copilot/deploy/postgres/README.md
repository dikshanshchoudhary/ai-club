# PostgreSQL schema

Apply `001_initial_schema.sql` to a PostgreSQL database before enabling persistence. The schema uses organization-scoped records and preserves audit history. Production deployments should use a migration tool, managed PostgreSQL, encrypted connections, backups, and least-privilege database credentials.

