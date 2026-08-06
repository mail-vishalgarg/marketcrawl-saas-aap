---
paths:
  - "backend/**/*.py"
  - "backend/**/*.toml"
  - "backend/**/*.ini"
---

# FastAPI Best Practices

## Project Layout

```
backend/app/
├── main.py              # App factory only — no routes here
├── routers/
│   └── products.py      # One file per resource
├── services/
│   └── products.py      # Business logic, one file per domain
├── models/
│   ├── request.py       # Pydantic input models
│   └── response.py      # Pydantic output models
├── dependencies.py      # Shared FastAPI Depends() callables
└── settings.py          # Pydantic Settings (reads from env)
```

## App Factory

`main.py` registers routers and nothing else:

```python
from fastapi import FastAPI
from app.routers import products, auth

def create_app() -> FastAPI:
    app = FastAPI(title="MarketCrawl SaaS")
    app.include_router(products.router, prefix="/products", tags=["products"])
    app.include_router(auth.router, prefix="/auth", tags=["auth"])
    return app

app = create_app()
```

## Routers — three lines, no more

A route handler does exactly: validate → call service → return.

```python
# routers/products.py
from fastapi import APIRouter, Depends
from app.models.request import ProductSearchRequest
from app.models.response import ProductSearchResponse
from app.services import products as svc
from app.dependencies import get_current_user

router = APIRouter()

@router.post("/search", response_model=ProductSearchResponse)
async def search_products(
    body: ProductSearchRequest,
    user: User = Depends(get_current_user),
) -> ProductSearchResponse:
    return await svc.search(body, user_id=user.id)
```

## Services — pure functions, no FastAPI imports

```python
# services/products.py
async def search(req: ProductSearchRequest, user_id: str) -> ProductSearchResponse:
    raw = await oxylabs.fetch_asins(req.query, req.marketplace)
    enriched = await openai.enrich(raw)
    await db.log_query(user_id, req.query)
    return ProductSearchResponse(results=enriched)
```

Services never import from `fastapi`. They raise `ValueError` / domain exceptions;
routers convert those to `HTTPException` if needed.

## Pydantic v2 Models

```python
from pydantic import BaseModel, ConfigDict, field_validator

class ProductSearchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    query: str
    marketplace: str = "amazon.com"
    max_results: int = 10

    @field_validator("max_results")
    @classmethod
    def cap_results(cls, v: int) -> int:
        if v > 50:
            raise ValueError("max_results cannot exceed 50")
        return v
```

- `extra="forbid"` on every model that receives external input.
- Validators are `@classmethod`; return the (possibly mutated) value.
- Use `model_config` not the deprecated inner `class Config`.

## Dependency Injection

Centralise all cross-cutting concerns in `dependencies.py`:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

bearer = HTTPBearer()

async def get_current_user(token: str = Depends(bearer)) -> User:
    payload = decode_jwt(token.credentials)  # raises on invalid
    user = await db.get_user(payload["sub"])
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    return user

async def get_settings() -> Settings:
    return Settings()  # reads env vars once, cached by FastAPI
```

## Settings — read from env, never hardcode

```python
# settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    oxylabs_username: str
    oxylabs_password: str
    jwt_secret: str
    database_url: str

    model_config = ConfigDict(env_file=".env", extra="ignore")
```

Inject via `Depends(get_settings)`, never import `Settings()` directly in routers.

## Error Handling

Register a global handler in `main.py`, not scattered `try/except` in services:

```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": str(exc)})
```

Only catch exceptions you can actually handle. Let others bubble to the global handler.

## Async vs Sync

- Use `async def` when the function does I/O (HTTP calls, DB queries).
- Use `def` for pure computation. FastAPI runs sync routes in a threadpool automatically.
- Never mix `asyncio.run()` inside an async route — it deadlocks.

## Testing

One test file per router; use `httpx.AsyncClient` against the real app:

```python
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}
```

- Test services independently of routers (they're plain async functions).
- No mocking of the database in service tests — use a test Supabase project or a local Postgres.
- Assert on the full response shape, not just the status code.
