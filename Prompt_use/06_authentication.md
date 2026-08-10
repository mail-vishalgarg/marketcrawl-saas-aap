# Level 5 — Authentication (Supabase Auth + JWT)

**Goal:** real sign-up / login. React gets a Supabase session (JWT); FastAPI verifies that
JWT on every dashboard request and resolves the caller's tenant.

## Prompt to paste into Claude Code

```text
Add end-to-end authentication using Supabase Auth.

Frontend (frontend/):
- Install @supabase/supabase-js; create src/lib/supabase.ts from VITE_SUPABASE_URL and
  VITE_SUPABASE_ANON_KEY.
- Wire the /login page to signInWithPassword and add a sign-up flow.
- Add an AuthContext/provider that tracks the session and redirects unauthenticated users to
  /login. Protect all dashboard routes.
- In src/lib/api.ts, attach the Supabase access token as `Authorization: Bearer <jwt>` on
  every backend call.

Backend (backend/app/):
- Implement security.py verify_jwt(token): validate the Supabase user token and return the
  user id (sub) and email. IMPORTANT: modern Supabase signs user access tokens with
  ASYMMETRIC keys (ES256), so verify against the project's JWKS endpoint
  (GET {SUPABASE_URL}/auth/v1/.well-known/jwks.json, sent with the apikey header) using
  jwt.PyJWKClient — NOT the legacy HS256 SUPABASE_JWT_SECRET. Requires PyJWT[crypto].
  Use audience="authenticated".
- Add a FastAPI dependency get_current_user that reads the Bearer token, verifies it, and
  returns the user; 401 on failure.
- Add a dependency get_current_tenant that loads (or lazily creates on first login) the
  tenant owned by the current user.
- Un-stub routers/tenants.py: GET /me/tenant returns the caller's tenant; enforce
  get_current_user everywhere a user context is needed.

Add tests: a request with no/invalid token gets 401; a valid token resolves a tenant.
```

## Acceptance criteria
- Sign up in the UI → session persists → dashboard loads; sign-out works.
- Backend rejects missing/invalid JWT with 401; valid JWT resolves the right tenant.
- First login auto-provisions a tenant row.

## Teaching notes
- This is **auth plane #1: humans with JWTs.** Contrast it later with API keys (machines).
- Show the token in the browser devtools Network tab riding along as `Authorization: Bearer`.
  Decode it on jwt.io to reveal `sub`, `exp` — demystifies "what is a JWT."
- Supabase issues and signs the token; our backend only *verifies* it. Separation of concerns.