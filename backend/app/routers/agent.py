from fastapi import APIRouter, Depends, Request

from app.dependencies import get_current_user
from app.limiter import limiter
from app.models.request import AnalysisRequest
from app.models.response import AgentHealthResponse, AnalysisResponse
from app.security import TokenClaims
from app.services.agent import run_analysis

router = APIRouter(prefix="/api/v1/agent", tags=["agent"])


@router.post("/analyze", response_model=AnalysisResponse)
@limiter.limit("10/minute")
async def analyze(
    request: Request,
    body: AnalysisRequest,
    _user: TokenClaims = Depends(get_current_user),
) -> AnalysisResponse:
    result = await run_analysis(question=body.question, marketplace=body.marketplace)
    return AnalysisResponse(
        analysis=result["analysis"],
        question=result["question"],
        marketplace=result["marketplace"],
    )


@router.get("/health", response_model=AgentHealthResponse)
async def agent_health() -> AgentHealthResponse:
    return AgentHealthResponse(
        status="ok",
        llm="gpt-4o",
        oxylabs="realtime.oxylabs.io",
    )
