from datetime import UTC, datetime

from pydantic import BaseModel, Field


class ProductCard(BaseModel):
    asin: str
    title: str
    price: str | None = None
    rating: float | None = None
    image_url: str | None = None


class AnalysisResponse(BaseModel):
    analysis: str
    question: str
    marketplace: str
    products: list[ProductCard] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class HealthResponse(BaseModel):
    status: str


class AgentHealthResponse(BaseModel):
    status: str
    llm: str
    oxylabs: str


class TenantResponse(BaseModel):
    id: str
    user_id: str
    name: str
    created_at: str


class ApiKeyResponse(BaseModel):
    id: str
    name: str
    key_prefix: str
    created_at: str
    last_used_at: str | None
    revoked: bool


class CreatedApiKeyResponse(ApiKeyResponse):
    raw_key: str
