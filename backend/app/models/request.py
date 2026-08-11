from pydantic import BaseModel, ConfigDict, Field


class CreateApiKeyRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., min_length=1, max_length=100, description="Human-readable key label")


class AnalysisRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question: str = Field(
        ...,
        min_length=5,
        max_length=500,
        description="Your Amazon competitive analysis question",
    )
    marketplace: str = Field(
        default="com",
        description="Amazon marketplace: com, co.uk, de, fr, ca",
    )
