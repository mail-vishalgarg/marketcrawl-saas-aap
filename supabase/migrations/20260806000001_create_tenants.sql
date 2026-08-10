-- Tenant provisioned automatically on first login.
-- One tenant per Supabase auth user.
CREATE TABLE IF NOT EXISTS tenants (
  id         uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id    uuid        NOT NULL UNIQUE REFERENCES auth.users(id) ON DELETE CASCADE,
  name       text        NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE tenants ENABLE ROW LEVEL SECURITY;

-- Users can only read their own tenant row via the anon/authenticated key.
-- The backend uses the service role key, which bypasses RLS entirely.
CREATE POLICY "users_select_own_tenant"
  ON tenants FOR SELECT
  USING (auth.uid() = user_id);
