Level 0 — Repo & Claude Code Setup
Goal: a clean monorepo with Claude Code configured (CLAUDE.md + rules) and airtight secret hygiene, before any product code exists.

Prompt to paste into Claude Code
Set up a fresh monorepo for a SaaS product called "MarketPulse" — an AI agent that scrapes
Amazon via Oxylabs and exposes it to customers through an authenticated API.

Create this structure (do NOT write feature code yet, just scaffolding):
  backend/    -> Python 3.12 + FastAPI, managed with uv (pyproject.toml)
  frontend/   -> React + Vite + TypeScript (npm create vite)
  supabase/   -> migrations/ folder (empty for now)
  docs/       -> keep existing files
  prompts/    -> keep existing files

Then create:
1. A root CLAUDE.md that documents: the product in 3 lines, the tech stack, the folder
   layout, how to run backend and frontend locally, and the golden rules (typed Python,
   small functions, no secrets in code, tests for business logic).
2. A .claude/rules/ folder with two short rule files:
   - security.md: never commit secrets; read config only from environment; hash API keys,
     never store them raw; validate all external input.
   - coding.md: FastAPI routers thin, logic in services; Pydantic models for all I/O;
     React components small and typed; conventional commits.
3. A .gitignore that ignores .env, .venv, node_modules, __pycache__, frontend/dist.
4. A .env.example listing every variable the app will need (OpenAI, Oxylabs, Supabase URL +
   keys, Postgres URI, JWT secret) with placeholder values and a comment each — but NO real
   secrets.
5. A minimal backend/app/main.py FastAPI app that only exposes GET /health returning
   {"status": "ok"}.

Finally, initialize git and make the first commit.
Acceptance criteria
backend/, frontend/, supabase/migrations/ exist; uv run uvicorn app.main:app serves /health.
CLAUDE.md + .claude/rules/*.md present and readable.
.env is git-ignored; .env.example has placeholders only.
Clean first commit.
Teaching notes
This is the "how Claude Code is configured" segment: CLAUDE.md = project memory Claude reads every session; .claude/rules/ = guardrails. Show that these steer the AI.
Secrets lesson: point at their own leaked .env on Desktop/saas-app — rotate any key that ever hit a screen-share. This is why rule #1 is "no secrets in code."