Level 2 — Backend Design (FastAPI)
Goal: a clean, layered FastAPI backend skeleton wired to Supabase Postgres — routers, services, config, DB access — ready for auth and features to plug in.

Prompt to paste into Claude Code
Build the FastAPI backend skeleton for MarketCrawl with a clean layered structure. No agent
or scraping logic yet — just the architecture other levels plug into.

Layout under backend/app/:
  main.py            FastAPI app, CORS, includes all routers, GET /health
  config.py          Pydantic BaseSettings reading .env (OpenAI, Oxylabs, Supabase URL +
                     anon + service-role keys, POSTGRES_URI, JWT_SECRET)
  db.py              A psycopg connection pool to POSTGRES_URI, plus a get_conn() dependency
  security.py        (stubs for now) verify_jwt(token) and require_api_key(...) placeholders
  models.py          Pydantic request/response models shared across routers
  routers/
    health.py        GET /health, GET /health/db (checks a SELECT 1)
    tenants.py       GET /me/tenant, POST /me/tenant (create tenant for current user) — stub
                     the auth for now, return 501 where auth is required
  services/
    tenants.py       tenant CRUD against Postgres (create, get_by_owner)

Rules:
- Routers are thin: parse input, call a service, return a model. No SQL in routers.
- All request/response bodies are typed Pydantic models.
- Config is read ONCE from env; nothing hardcoded.
- Add a backend/README.md with run instructions (uv run uvicorn app.main:app --reload --port 8010).

Add a couple of pytest tests for /health and the tenants service (use a test Postgres or mock).
Acceptance criteria
GET /health and GET /health/db both succeed against Supabase.
Clear separation: routers/ (thin) → services/ (logic) → db.py (access).
config.py fails loudly if a required env var is missing.
Tests pass.
Teaching notes
Teach layering: why SQL doesn't belong in a route handler (testability, reuse, swapability).
config.py as the single source of truth for env — show how the same code runs locally and on Cloud Run just by changing environment variables.
The security.py stubs are deliberate seams — levels 4 and 5 fill them in.