# Level 8 — Public Developer API

**Goal:** the endpoint customers call *from their own backend* with an API key. This is the
product's public surface — the reason they pay.

## Prompt to paste into Claude Code

```text
Expose MarketPulse's capability as a versioned public API that customers call with their
API key (not a JWT). The agent itself lands in Level 9; here, build the API contract and
guard rails, calling a placeholder extract service that returns a stub for now.

Backend (backend/app/):
- routers/v1.py, mounted at /v1, every route protected by BOTH require_api_key AND
  enforce_rate_limit (from Levels 6 and 7):
  - POST /v1/extract
      body: { "query": str, "marketplace": str = "in", "max_results": int = 8 }
      calls services/extract.run(query, ...) -> structured JSON of products
      returns { "request_id", "results": [...], "usage": {used, limit} }
  - GET /v1/health  (key-authed ping)
- services/extract.py: for now, a stub run() returning a couple of fake products. Level 9
  replaces its body with the real agent — keep the signature stable.
- Consistent error envelope for 401 (bad key), 429 (quota), 422 (bad input), 500.
- Auto-generated OpenAPI docs at /docs; make sure the api-key security scheme shows there.

Frontend (frontend/):
- Fill in the /docs developer page with real, copy-pasteable curl / Python / JavaScript
  snippets that hit POST /v1/extract with the user's key and the correct base URL.

Tests: no key -> 401; valid key -> 200 with the envelope; over quota -> 429.
```

## Acceptance criteria
- `POST /v1/extract` works with a real API key from Level 6 and respects the Level 7 quota.
- Wrong/missing key → 401; over quota → 429; bad body → 422 — all in a consistent envelope.
- `/docs` shows the API-key scheme; the frontend snippets actually run.

## Teaching notes
- **This is the product.** Show a student calling it from a *separate* terminal/script with
  just a key — no login, no browser. That's "API for their backend."
- Versioning (`/v1`) and a stable service signature = you can swap the stub for the real agent
  in Level 9 without breaking callers. Teach the seam.
- The same request now flows through both planes' machinery: key auth → rate limit → work → log.