-- API keys issued to tenants for machine-to-machine auth.
-- Only key_hash is stored — the raw key is shown once on creation.
CREATE TABLE IF NOT EXISTS api_keys (
  id           uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id    uuid        NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  name         text        NOT NULL,
  key_prefix   text        NOT NULL,
  key_hash     text        NOT NULL UNIQUE,
  created_at   timestamptz NOT NULL DEFAULT now(),
  last_used_at timestamptz,
  revoked      boolean     NOT NULL DEFAULT false
);

ALTER TABLE api_keys ENABLE ROW LEVEL SECURITY;

-- Fast lookup by tenant (list view) and by hash (verify path).
CREATE INDEX ON api_keys (tenant_id);
CREATE INDEX ON api_keys (key_hash) WHERE NOT revoked;

-- Dashboard users can manage their own tenant's keys.
-- The backend uses the service role key which bypasses RLS entirely.
CREATE POLICY "tenants_manage_own_keys"
  ON api_keys FOR ALL
  USING (tenant_id IN (SELECT id FROM tenants WHERE user_id = auth.uid()));
