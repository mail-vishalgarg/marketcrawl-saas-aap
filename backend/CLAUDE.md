<!-- This file loads on demand when Claude reads any file inside backend/. -->
<!-- Keep it under 100 lines. Deep FastAPI conventions live in .claude/rules/fastapi.md. -->

# Backend

## Commands

```bash
uv sync                                                      # install / sync deps
uv run uvicorn app.main:app --reload --port 8000             # dev server
uv run pytest                                                # run tests
uv run ruff format app/ && uv run ruff check app/            # format + lint
uv run pyright app/                                          # type check (strict)
```

## Layout

```
app/
├── main.py           # create_app() — registers routers, nothing else
├── routers/          # one file per resource; handlers are 3-5 lines
├── services/         # all business logic; no FastAPI imports allowed here
├── models/
│   ├── request.py    # Pydantic v2 input models (extra="forbid")
│   └── response.py   # Pydantic v2 output models
├── dependencies.py   # shared Depends() callables (auth, settings, db)
└── settings.py       # pydantic-settings; reads from env vars only
```

## Non-obvious decisions

- `uv run` (not `python`) — ensures the venv is always activated.
- `PYTHONPATH=/app` is set in Docker so `app.main` resolves without installing as a package.
- `pyright` strict mode is enforced in CI — fix all type errors before opening a PR.
- Services raise plain `ValueError`; a global handler in `main.py` converts to HTTP 422.
