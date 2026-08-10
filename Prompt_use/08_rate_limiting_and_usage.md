# Level 7 — Rate Limiting & Usage Metering

**Goal:** every API call is logged and counted against the tenant's daily quota. This is the
business core — it protects your Oxylabs/OpenAI spend.

## Prompt to paste into Claude Code

```text
Add per-tenant usage metering and daily rate limiting to MarketPulse.

Backend (backend/app/):
- services/usage.py:
  - log_usage(tenant_id, api_key_id, endpoint, status_code): insert a usage_logs row.
  - usage_today(tenant_id): count today's usage_logs (reuse the SQL helper from Level 2).
  - check_quota(tenant_id): load tenants.daily_quota, compare to usage_today; return
    (allowed: bool, used: int, limit: int).
- A FastAPI dependency enforce_rate_limit that runs after require_api_key: if over quota,
  return HTTP 429 with a JSON body {error, used, limit, reset_at} and the standard headers
  X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset. Always log the call (including
  the 429) via log_usage.
- Add GET /me/usage (JWT-protected): returns today's usage, the quota, and a 14-day daily
  series for a chart.

Frontend (frontend/):
- Overview page: real usage-vs-quota progress bar from /me/usage, plus a small 14-day bar chart.

Tests: calls under the limit pass and are logged; the call that crosses the limit returns 429
with correct headers; usage_today reflects the logs.
```

## Acceptance criteria
- The N+1th call in a day (quota N) returns **429** with rate-limit headers.
- Every call — success or 429 — appears in `usage_logs`.
- The dashboard shows real usage vs quota.

## Teaching notes
- **This is the "why" of the whole SaaS.** Each call spends real Oxylabs credits; the quota is
  what stands between you and a surprise bill. Students finally feel *why* keys + limits exist.
- Show the 429 live: set a tiny quota (e.g. 3), call 4 times with curl, watch it block.
- Mention next steps for scale (Redis counter, sliding window) but keep the DB-count version —
  it's the most teachable and correct for the class scale.