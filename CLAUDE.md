# MarketCrawl SaaS

MarketCrawl SaaS is an AI agent that scrapes Amazon product data via Oxylabs, enriches it
with OpenAI, and exposes it to customers through a JWT-authenticated REST API.
Customers query our API for real-time Amazon pricing, reviews, and trends — without touching
Amazon directly.
The backend is a Python/FastAPI service; the frontend is a React dashboard for managing API
keys and viewing usage analytics.

## Tech Stack

| Layer      | Technology                              |
|------------|-----------------------------------------|
| Backend    | Python 3.12, FastAPI, Pydantic v2, uv   |
| Database   | Supabase (Postgres)                     |
| Auth       | Supabase Auth + JWT                     |
| Scraping   | Oxylabs Realtime Scraper API            |
| AI         | OpenAI API                              |
| Frontend   | React 18, Vite, TypeScript (strict)     |
| Infra      | Docker, Google Cloud Run                |

## Folder Layout

```
marketcrawl-saas/
├── backend/              # Python FastAPI service
│   ├── app/
│   │   ├── main.py       # FastAPI entry point
│   │   ├── routers/      # Thin route handlers
│   │   └── services/     # Business logic lives here
│   └── pyproject.toml
├── frontend/             # React + Vite + TypeScript dashboard
│   └── src/
├── supabase/
│   └── migrations/       # SQL migrations (applied via Supabase CLI)
├── docs/                 # Architecture diagrams, API docs
└── prompts/              # LLM prompt templates
```

## Live API (Production)

Base URL: `https://marketcrawl-saas-3bgctxs6tq-wl.a.run.app`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check — `{"status": "ok"}` |
| GET | `/docs` | Swagger UI (interactive API explorer) |
| GET | `/redoc` | ReDoc (alternative API reference) |

## Running Locally

### Backend

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload --port 8000
```

Visit http://localhost:8000/health to verify.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Visit http://localhost:5173 for the dev server.

## Golden Rules

1. **Typed Python** — every function has type annotations; `pyright` strict mode must pass.
2. **Small functions** — aim for ≤30 lines per function; extract helpers early.
3. **No secrets in code** — all config read from environment variables (see `.env.example`).
4. **Tests for business logic** — every function in `services/` needs a pytest test.
