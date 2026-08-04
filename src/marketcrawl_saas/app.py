from fastapi import FastAPI
from pydantic import BaseModel
import importlib.metadata

app = FastAPI(title="MarketCrawl SaaS", version=importlib.metadata.version("marketcrawl-saas"))


class HealthResponse(BaseModel):
    status: str
    version: str
    service: str


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        version=app.version,
        service=app.title,
    )
