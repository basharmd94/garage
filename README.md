# FastAPI RBAC Starter

JWT auth + refresh tokens, DB-driven RBAC via `permissions.allowed_groups` (CSV),
and multi-image support for Customers and Items (URLs or file uploads).

## Quickstart

1. Create Postgres DB and set env vars (optional defaults in code).
2. Install deps:
   ```bash
   pip install -r requirements.txt
