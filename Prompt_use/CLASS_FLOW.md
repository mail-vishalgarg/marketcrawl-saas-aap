# Class Run-of-Show

The live sequence for teaching the build. Each step maps to a prompt file (or a talk/do
moment). The spine: **frame it → stand up infra & prove CI/CD → then build the app.**

## Phase A — Frame it (talk, ~10 min)
1. **Explain the product & goal.** MarketPulse: a SaaS where customers sign up, get an API
   key, and call our AI extraction API from their own backend. We build it end-to-end, fast.
2. **Show the architecture.** Walk `docs/ARCHITECTURE.md` — the diagram, the two auth planes
   (JWT for humans, API keys for machines), and why rate limits exist (upstream costs money).

## Phase B — Infra first (do, ~25 min)
3. **What infra we need.** Checklist: GitHub repo, Supabase (Postgres+Auth), Google Cloud
   (Cloud Run), OpenAI key, Oxylabs (optional — mock mode covers it).
4. **Set up the GitHub repo.** Create it; clone; empty commit.
5. **Set up `CLAUDE.md`.** → `prompts/00_repo_and_claude_setup.md` (the CLAUDE.md part).
6. **Set up the Claude rules.** → same prompt, the `.claude/rules/` part. Explain how these
   steer Claude Code.
7. **Set up the GitHub Actions pipeline.** → `prompts/01_cicd_pipeline.md`.
8. **Create a basic API endpoint** (`GET /health`) so Cloud Run has something to run.
   (Already scaffolded in Level 0; Level 1 containerizes + deploys it.)
9. **Everything syncs to Google Cloud.** First deploy lands; open the live Cloud Run URL.
10. **Make a change.** Edit the `/health` response; commit + push.
11. **Watch it roll out.** GitHub Action runs → Cloud Run redeploys → refresh the URL.
    *This is the "CI/CD is live and syncing" payoff.*

## Phase C — Build the application (do, the main event)
12. **Give the prompts, and it builds.** Go level by level; each ends with a push that
    auto-deploys through the pipeline you just proved:
    - `02_infra_supabase.md` — database schema + RLS
    - `03_backend_design.md` — FastAPI structure
    - `04_ui_design.md` — React dashboard + developer view
    - `05_authentication.md` — sign-up / login (JWT)
    - `06_api_keys.md` — mint & manage keys
    - `07_rate_limiting_and_usage.md` — daily quota + metering
    - `08_developer_api.md` — public `POST /v1/extract`
    - `09_agent_features.md` — the real agent (uses `reference/marketpulse_prompts.md`)

## Closing demo
- Sign up as a new "customer" → mint a key → call `POST /v1/extract` from a separate terminal
  → show usage tick up → set a tiny quota → hit **429**. The full SaaS loop in 2 minutes.

## Timing tip
If short on time, Phase C can stop after Level 8 (a working keyed API on the stub) and treat
Level 9 (the agent) as the "and here's the real intelligence" finale or a follow-up session.