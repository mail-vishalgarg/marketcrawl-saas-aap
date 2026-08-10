Level 1 — Infra: Supabase (Database + Schema + RLS)
Goal: a real managed Postgres on Supabase with the SaaS multi-tenant schema and Row-Level Security, delivered as a versioned migration.

Before the prompt (do live in class)
Create a Supabase project at supabase.com (free tier).
Copy into .env: SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY, and the Postgres connection string as POSTGRES_URI.
Prompt to paste into Claude Code
Design the multi-tenant database schema for MarketPulse and write it as a Supabase migration
at supabase/migrations/0001_init.sql. Supabase already gives us auth.users.

Tables:
1. tenants
   - id uuid primary key default gen_random_uuid()
   - owner_id uuid not null references auth.users(id) on delete cascade
   - name text not null
   - plan text not null default 'free'
   - daily_quota int not null default 100   -- max API calls per day
   - created_at timestamptz not null default now()
2. api_keys
   - id uuid primary key default gen_random_uuid()
   - tenant_id uuid not null references tenants(id) on delete cascade
   - name text not null
   - key_prefix text not null        -- first 8 chars, safe to display
   - key_hash text not null          -- sha256 of the full key; NEVER the raw key
   - last_used_at timestamptz
   - revoked boolean not null default false
   - created_at timestamptz not null default now()
3. usage_logs
   - id bigint generated always as identity primary key
   - tenant_id uuid not null references tenants(id) on delete cascade
   - api_key_id uuid references api_keys(id) on delete set null
   - endpoint text not null
   - status_code int not null
   - created_at timestamptz not null default now()
   - index on (tenant_id, created_at)

Enable Row-Level Security on all three tables. Policies:
- A logged-in user can SELECT/INSERT/UPDATE/DELETE their own tenants (owner_id = auth.uid()).
- api_keys and usage_logs are readable only when their tenant belongs to auth.uid().
- The backend uses the service-role key and bypasses RLS for the public API path.

Also write a SQL helper function usage_today(tenant uuid) returning the count of usage_logs
for that tenant since midnight UTC — we'll use it for rate limiting.

Explain in comments how to apply the migration (Supabase SQL editor or CLI).
Acceptance criteria
0001_init.sql applies cleanly in the Supabase SQL editor.
RLS is ON; a user querying with the anon key sees only their own rows.
select usage_today('<tenant-id>') returns a number.
Teaching notes
RLS is multi-tenancy enforced by the database, not the app — tenant A physically cannot read tenant B. This is the single most important SaaS-security idea in the course.
Note the two access modes: dashboard reads go through anon key + user JWT (RLS applies); the public API path uses the service-role key (RLS bypassed, we enforce rules in code).
key_hash, never the raw key: if the DB leaks, keys are useless. Preview shown via key_prefix.