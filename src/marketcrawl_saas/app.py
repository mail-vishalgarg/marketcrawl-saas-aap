import importlib.metadata

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="MarketCrawl SaaS", version=importlib.metadata.version("marketcrawl-saas")
)


class HealthResponse(BaseModel):
    status: str
    version: str
    service: str


class StatusResponse(BaseModel):
    message: str
    version: str
    live: bool


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        version=app.version,
        service=app.title,
    )


@app.get("/status", response_model=StatusResponse)
def status() -> StatusResponse:
    return StatusResponse(
        message="MarketCrawl SaaS is up and running!",
        version=app.version,
        live=True,
    )
