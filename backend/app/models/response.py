from datetime import datetime, timezone

from pydantic import BaseModel, Field


class AnalysisResponse(BaseModel):
    analysis: str
    question: str
    marketplace: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class HealthResponse(BaseModel):
    status: str


class AgentHealthResponse(BaseModel):
    status: str
    llm: str
    oxylabs: str
