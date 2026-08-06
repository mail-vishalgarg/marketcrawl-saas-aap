# Coding Rules

- **FastAPI routers stay thin.** Route handlers do exactly three things: validate input,
  call one service function, return the result. No business logic in routers.
- **Logic lives in services.** Put all domain logic in `backend/app/services/`; routers
  import from there. Services are plain Python functions, not FastAPI-aware.
- **Pydantic models for all I/O.** Request bodies, response bodies, and inter-service data
  all use typed Pydantic v2 models — never raw `dict`.
- **React components stay small.** Each component has one responsibility and fits on a
  screen (~50 lines). Shared logic goes into hooks (`src/hooks/`) or utility modules
  (`src/lib/`).
- **TypeScript strict mode everywhere.** No `any`; prop types on every component; `strict:
  true` in `tsconfig.json`.
- **Conventional commits.** Format: `type(scope): description` — e.g.
  `feat(scraper): add ASIN batch endpoint`, `fix(auth): handle expired JWT edge case`.
  Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`.
