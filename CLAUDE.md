<!--
  MAINTAINER NOTES (stripped from Claude's context — free to edit)
  ─────────────────────────────────────────────────────────────────
  Memory architecture for this repo:

  LOADS EVERY SESSION (always in context):
    CLAUDE.md                   ← this file  (project-wide rules)
    CLAUDE.local.md             ← personal overrides, gitignored
    .claude/rules/coding.md     ← general coding standards
    .claude/rules/security.md   ← security requirements

  LOADS ON DEMAND (when Claude reads matching files):
    .claude/rules/fastapi.md    ← paths: backend/**/*.py  (via paths: frontmatter)
    .claude/rules/react.md      ← paths: frontend/**/*.{ts,tsx,css,json}
    backend/CLAUDE.md           ← when Claude opens any file inside backend/
    frontend/CLAUDE.md          ← when Claude opens any file inside frontend/
    supabase/CLAUDE.md          ← when Claude opens any file inside supabase/

  TEAM-SHARED MEMORY (committed, updated as the project evolves):
    .claude/memory/MEMORY.md    ← index (max 200 lines loaded at session start)
    .claude/memory/*.md         ← detail files, loaded on demand by Claude

  TO ADD A NEW RULE:
    - Applies to the whole project → add to this file or .claude/rules/coding.md
    - Applies to a specific stack  → add to .claude/rules/fastapi.md or react.md
    - Applies to a subdirectory    → add to that directory's CLAUDE.md
    - A decision worth remembering → add to .claude/memory/ (survives /compact)

  Keep this file under 150 lines. Run `/doctor` to check for trim opportunities.
-->

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

<!-- Folder layout kept intentionally — orients new teammates faster than `ls`. -->
## Folder Layout

```
marketcrawl-saas/
├── backend/              # Python FastAPI service  → see backend/CLAUDE.md
├── frontend/             # React + Vite dashboard  → see frontend/CLAUDE.md
├── supabase/migrations/  # SQL migrations          → see supabase/CLAUDE.md
├── docs/                 # Architecture diagrams, API docs
├── prompts/              # LLM prompt templates
└── .claude/rules/        # Coding + security rules (auto-loaded by Claude)
```

## Live API (Production)

Base URL: `https://marketcrawl-saas-3bgctxs6tq-wl.a.run.app`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check — `{"status": "ok"}` |
| GET | `/docs` | Swagger UI (interactive API explorer) |
| GET | `/redoc` | ReDoc (alternative API reference) |

## Running Locally

```bash
# Backend
cd backend && uv sync && uv run uvicorn app.main:app --reload --port 8000
# → http://localhost:8000/health

# Frontend
cd frontend && npm install && npm run dev
# → http://localhost:5173
```

## Golden Rules

1. **Typed Python** — every function has type annotations; `pyright` strict mode must pass.
2. **Small functions** — aim for ≤30 lines; extract helpers early.
3. **No secrets in code** — all config from environment variables (see `.env.example`).
4. **Tests for business logic** — every function in `services/` needs a pytest test.
