Level 4 — UI Design (React + Vite Dashboard)
Goal: the customer-facing dashboard SPA — where users log in, chat with the agent, mint API keys, and watch usage. Build the shell and design system first; auth and data wire in at later levels.

Prompt to paste into Claude Code
Build the frontend/ dashboard for MarketPulse as a React + Vite + TypeScript SPA. Design a
clean, modern developer-tool aesthetic (think Vercel / Supabase dashboards): dark sidebar,
light content area, generous spacing, a single accent color, system font stack. Use plain
CSS or CSS modules — no heavy UI kit.

Pages / routes (react-router):
1. /login        Email + password form (Supabase Auth wires in at Level 5 — stub the call).
2. /             Overview: greeting, today's usage vs daily quota (progress bar), recent
                 activity list. Use mock data for now.
3. /playground   A chat panel: message list with user/assistant bubbles, an input box, and a
                 right-hand "results" area for product cards and an image gallery. This is the
                 agent UI. Wire to POST /chat later; mock responses for now.
4. /api-keys     Table of API keys (name, prefix, created, last used, revoke button) and a
                 "Create key" modal that shows the raw key ONCE with a copy button.
5. /docs         A simple developer view: a code snippet showing how to call our public API
                 with an API key (curl + Python + JavaScript tabs).

Also:
- A shared layout with sidebar nav and the signed-in user's email + sign-out.
- A typed api client module (src/lib/api.ts) with a fetch wrapper that will attach the auth
  token; centralize the backend base URL from an env var (VITE_API_URL).
- Loading and empty states everywhere.
- frontend/Dockerfile that builds the static site and serves it (nginx) for Cloud Run.

Keep components small and typed. Everything data-driven should read from the api client so we
can swap mocks for real calls with minimal changes.

Acceptance criteria
npm run dev renders all 5 routes with mock data and a coherent look.
API base URL comes from VITE_API_URL, not hardcoded.
The "create key → shown once" and "usage vs quota" UIs exist (even on mock data).

notes
Point out the developer view (/docs, /api-keys) — this is what makes it a product for developers, not just an app. It's what the customer sees.
The "raw key shown once" pattern is a security UX convention worth calling out — mirrors the key_hash-only storage from Level 2.
Mock-first UI = you can teach layout/UX before the backend is ready; wiring is a small diff later.