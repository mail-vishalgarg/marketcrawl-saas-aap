# Prompt Pack — Build an AI SaaS with Claude Code

A set of **paste-ready prompts**, one per level. Hand a student (or paste yourself) the
prompt for the level you're on, and Claude Code builds that piece. Built **infra-first**:
plumbing and deploy come before features, so every feature lands in a pipeline that's
already live.

**Product being built:** *MarketPulse* — a SaaS around an AI agent that scrapes Amazon
(via Oxylabs) and answers market-research questions. Customers sign up, get an **API key**,
and call our extraction API from their own backend. Rename freely.

**Seed / prototype:** the `marketpulse` reference project. Its best assets — the agent
system prompt and the 4 tool designs — are extracted verbatim in
[`reference/marketpulse_prompts.md`](reference/marketpulse_prompts.md). Everything else is
built fresh.

## The levels (give in this order)

Infra and the CI/CD pipeline come **first** — deploy a bare endpoint, prove it syncs, then
build features into a live pipeline. See [`CLASS_FLOW.md`](CLASS_FLOW.md) for the live
run-of-show mapped to class steps.

| # | File | Builds | Type |
|---|---|---|---|
| 0 | `00_repo_and_claude_setup.md` | Repo, `CLAUDE.md`, rules, `.env.example`, `/health` | Infra |
| 1 | `01_cicd_pipeline.md` | Docker + GitHub Actions → Cloud Run (prove sync) | Infra / Deploy |
| 2 | `02_infra_supabase.md` | Supabase schema + RLS | Infra / DB |
| 3 | `03_backend_design.md` | FastAPI backend skeleton & structure | Backend |
| 4 | `04_ui_design.md` | React + Vite dashboard + developer view | UI |
| 5 | `05_authentication.md` | Supabase Auth (sign-up/login, JWT) | Auth |
| 6 | `06_api_keys.md` | Generate / hash / manage API keys | Auth |
| 7 | `07_rate_limiting_and_usage.md` | Per-tenant daily quota + usage logs | SaaS |
| 8 | `08_developer_api.md` | Public `POST /v1/extract` (key-auth) | SaaS |
| 9 | `09_agent_features.md` | The agent + 4 scraping tools + memory | Features |

> **Why this order:** the pipeline (Level 1) is proven before any feature exists, so every
> later `git push` auto-deploys — the "CI/CD is syncing" demo happens early and repeats.

## How to use each prompt

1. Open Claude Code in the repo root.
2. Copy the **"Prompt to paste"** block from the level's file.
3. Let Claude Code plan + build; review the diff together.
4. Check it against the **Acceptance criteria**.
5. Use the **Teaching notes** to explain *why* to the room.

## Stack (keep consistent across prompts)
Python **FastAPI** · **LangGraph** agent · **OpenAI** · **Oxylabs** (mock-mode fallback) ·
**Supabase** (Postgres + Auth) · **React + Vite** · **Google Cloud Run** · **GitHub Actions**.