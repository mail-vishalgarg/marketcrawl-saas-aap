<!-- This file loads on demand when Claude reads any file inside supabase/. -->

# Supabase / Migrations

## Commands (requires Supabase CLI: `brew install supabase/tap/supabase`)

```bash
supabase migration new <snake_case_name>   # creates migrations/<ts>_<name>.sql
supabase db push                           # apply pending migrations to remote project
supabase db reset                          # reset local DB and replay all migrations
supabase gen types typescript --local      # regenerate TypeScript types after schema change
```

Generated types go in `frontend/src/types/supabase.ts` — commit them with the migration.

## Conventions

- Migration files are **forward-only**: never edit a file that has been applied to any env.
- Add a header comment to every migration:
  ```sql
  -- Migration: add_products_table
  -- Why: store scraped Amazon product data per API key
  -- Affects: products table (new), api_keys table (fk)
  ```
- One logical change per migration file.
- After `supabase db reset` passes locally, run `supabase db push` to staging, then prod.
- Never store Supabase service-role key in code — inject via `SUPABASE_SERVICE_ROLE_KEY` env var.
