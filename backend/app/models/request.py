from pydantic import BaseModel, ConfigDict, Field


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
