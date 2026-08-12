import logging

from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.models.response import TenantResponse
from app.security import TokenClaims, verify_jwt
from app.services import api_keys as api_keys_svc
from app.services import tenants as tenants_svc

logger = logging.getLogger(__name__)
bearer = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> TokenClaims:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")
    try:
        return verify_jwt(credentials.credentials)
    except Exception as exc:
        logger.warning("JWT verification failed: %s", exc)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


async def get_current_tenant(
    user: TokenClaims = Depends(get_current_user),
) -> TenantResponse:
    return await tenants_svc.get_or_create(user_id=user.sub, email=user.email)


async def require_api_key(
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> str:
    """Accept mp_live_ key from X-API-Key header or Authorization: Bearer.
    Returns the tenant_id associated with the key."""
    raw_key: str | None = None
    if x_api_key and x_api_key.startswith("mp_live_"):
        raw_key = x_api_key
    elif credentials and credentials.credentials.startswith("mp_live_"):
        raw_key = credentials.credentials

    if not raw_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing API key")

    tenant_id = await api_keys_svc.verify_key(raw_key)
    if tenant_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or revoked API key"
        )
    return tenant_id
