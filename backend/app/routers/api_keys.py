from fastapi import APIRouter, Depends

from app.dependencies import get_current_tenant
from app.models.request import CreateApiKeyRequest
from app.models.response import ApiKeyResponse, CreatedApiKeyResponse, TenantResponse
from app.services import api_keys as svc

router = APIRouter(prefix="/api/v1/api-keys", tags=["api-keys"])


@router.get("", response_model=list[ApiKeyResponse])
async def list_api_keys(
    tenant: TenantResponse = Depends(get_current_tenant),
) -> list[ApiKeyResponse]:
    keys = await svc.list_keys(tenant.id)
    return [ApiKeyResponse.model_validate(k.model_dump()) for k in keys]


@router.post("", response_model=CreatedApiKeyResponse, status_code=201)
async def create_api_key(
    body: CreateApiKeyRequest,
    tenant: TenantResponse = Depends(get_current_tenant),
) -> CreatedApiKeyResponse:
    raw, meta = await svc.create_key(tenant.id, body.name)
    return CreatedApiKeyResponse(raw_key=raw, **meta.model_dump())


@router.delete("/{key_id}", status_code=204)
async def revoke_api_key(
    key_id: str,
    tenant: TenantResponse = Depends(get_current_tenant),
) -> None:
    await svc.revoke_key(tenant.id, key_id)
