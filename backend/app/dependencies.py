from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.models.response import TenantResponse
from app.security import TokenClaims, verify_jwt
from app.services import tenants as tenants_svc

bearer = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> TokenClaims:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")
    try:
        return verify_jwt(credentials.credentials)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


async def get_current_tenant(
    user: TokenClaims = Depends(get_current_user),
) -> TenantResponse:
    return await tenants_svc.get_or_create(user_id=user.sub, email=user.email)
