from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.limiter import limiter
from app.routers import agent as agent_router
from app.routers import api_keys as api_keys_router
from app.routers import tenants as tenants_router

app = FastAPI(
    title="MarketCrawl SaaS",
    description="Amazon competitive analysis API",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agent_router.router)
app.include_router(tenants_router.router)
app.include_router(api_keys_router.router)


class HealthResponse(BaseModel):
    status: str


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")
