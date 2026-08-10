# Level 6 — API Keys (Generate, Hash, Manage)

**Goal:** tenants mint API keys in the dashboard. We show the raw key **once**, store only its
hash, and can verify + revoke keys. This is what customers use to call us from their backend.

## Prompt to paste into Claude Code

```text
Implement API key management for MarketPulse.

Backend (backend/app/):
- services/api_keys.py:
  - generate_key(): create a key like "mp_live_" + 32 url-safe random chars. Compute
    sha256(key) as key_hash and key[:11] as key_prefix.
  - create_key(tenant_id, name): insert (tenant_id, name, key_prefix, key_hash), return the
    RAW key exactly once (never stored).
  - list_keys(tenant_id): return metadata only (id, name, prefix, created_at, last_used_at,
    revoked) — never hashes.
  - revoke_key(tenant_id, key_id): set revoked=true.
  - verify_key(raw_key) -> tenant_id | None: hash the incoming key, look up a non-revoked row,
    update last_used_at. Use a constant-time comparison. Uses the service-role DB access.
- routers/api_keys.py (JWT-protected, current tenant):
  - GET /api-keys, POST /api-keys {name}  (returns raw key once), DELETE /api-keys/{id}
- Fill in security.py require_api_key: a dependency that reads the "Authorization: Bearer
  mp_live_..." OR an "X-API-Key" header, calls verify_key, and returns the tenant_id; 401 if
  invalid. (Used by the public API in Level 8.)

Frontend (frontend/):
- Wire the /api-keys page to these endpoints. On create, show the raw key in a modal with a
  copy button and a clear "you won't see this again" warning. Then it disappears.

Tests: create → verify with raw key succeeds → revoke → verify now fails. Wrong key = 401.
```

## Acceptance criteria
- Creating a key shows the raw value once; refetching lists never expose the hash or raw key.
- `verify_key` accepts a valid key, rejects revoked/unknown keys, updates `last_used_at`.
- Revoke immediately invalidates the key.

## Teaching notes
- **Auth plane #2: machines with API keys.** Now both planes exist — put them side by side and
  explain when each is used (dashboard = JWT; programmatic API = key).
- Why hash + prefix: same reasoning as passwords. Show that even *you* can't recover a lost key
  — the customer must roll a new one. That's a feature, not a bug.
- Constant-time compare + service-role lookup: small details that make it production-grade.