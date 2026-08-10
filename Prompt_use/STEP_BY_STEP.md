# Class Run-of-Show — the 14 steps

The exact order to teach, mapped to the paste-ready prompt for each step. The spine is
**infra first**: set up the repo, config, and a working deploy pipeline BEFORE building any
feature — so every feature you add just rides the pipeline and can't break the foundation.

> Before class: open `diagrams/` (architecture, auth, DB, roles, CI/CD) and walk the big
> picture. Have the credential `user-guides/` open so you can show where each key comes from.

| # | Step | Do this | Prompt / guide |
|---|---|---|---|
| 1 | **Monorepo structure** | Create `backend/`, `frontend/`, `supabase/`, `docs/`, `.claude/` | `00_repo_and_claude_setup.md` |
| 2 | **CLAUDE.md, rules, conventions** | Add `CLAUDE.md` + `.claude/rules/*.md`; explain how they steer Claude Code | `00_repo_and_claude_setup.md` + `.claude/rules/` |
| 3 | **Initialize the GitHub repo** | `git init`, first commit, create the repo | `user-guides/05_github_secrets.md` |
| 4 | **Google Cloud secrets** | Create GCP project, billing, APIs, Artifact Registry, service account + key → GitHub Secrets | `01_cicd_pipeline.md` + `user-guides/04_google_cloud.md` + `docs/CICD_SETUP_GUIDE.md` |
| 5 | **Push → live URL** | Deploy a bare `GET /health`; get the public Cloud Run URL | `01_cicd_pipeline.md` |
| 6 | **Bump version → show redeploy** | Change the `/health` message, `git push`, watch it auto-deploy | `01_cicd_pipeline.md` (Part 6) |
| 7 | **Build the FastAPI backend** | Supabase DB + layered backend (config, db pool, services, routers) | `02_infra_supabase.md`, `03_backend_design.md` |
| 8 | **Build the React UI** | Vite dashboard shell (login, layout, api client) | `04_ui_design.md` |
| 9 | **Core features** | Auth: Supabase login → JWT → tenant | `05_authentication.md` |
| 10 | **API key management** | Customers mint keys + call the public `/v1` API | `06_api_keys.md`, `08_developer_api.md` |
| 11 | **Usage tracking** | Log every call; usage vs quota; the 429 | `07_rate_limiting_and_usage.md` |
| 12 | **Admin & customer views** | Role-based dashboards (`ADMIN_EMAILS`, `/me` is_admin, `/admin/*`) | *(see `concepts/05_admin_vs_customer.md`)* |
| 13 | **Test everything locally** | Run backend + frontend locally against the cloud DB; exercise the flows | `CLAUDE.md` run section |
| 14 | **Push to production** | `git push` → both Cloud Run services redeploy | `01_cicd_pipeline.md` |

## The one line to repeat
> "In any production app you set up the **repository and infrastructure first** so a broken
> feature can't take down the foundation — then you build features into a pipeline that
> already works." (Steps 1–6 are the foundation; 7–14 are features on top.)

## The finale demo (all live)
Sign up → mint a key → **Playground**: type a query → live Amazon products, quota ticks down →
hit **429** → **Upgrade → Pay** → quota jumps → log in as **admin** → see every tenant, upgrade
anyone. Then show the DB: it's one `plan` value flipping.