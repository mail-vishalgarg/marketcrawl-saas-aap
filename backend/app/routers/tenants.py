from fastapi import APIRouter, Depends

from app.dependencies import get_current_tenant
from app.models.response import TenantResponse

router = APIRouter(prefix="/api/v1", tags=["tenants"])


@router.get("/me/tenant", response_model=TenantResponse)
async def get_my_tenant(
    tenant: TenantResponse = Depends(get_current_tenant),
) -> TenantResponse:
    return tenant
