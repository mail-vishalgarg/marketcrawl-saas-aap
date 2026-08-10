from functools import lru_cache

from jwt import PyJWKClient, decode
from jwt.exceptions import PyJWTError
from pydantic import BaseModel

from app.settings import get_settings


class TokenClaims(BaseModel):
    sub: str
    email: str


@lru_cache(maxsize=1)
def _jwks_client() -> PyJWKClient:
    s = get_settings()
    return PyJWKClient(
        f"{s.supabase_url}/auth/v1/.well-known/jwks.json",
        headers={"apikey": s.supabase_anon_key},
    )


def verify_jwt(token: str) -> TokenClaims:
    """Validate a Supabase access token (ES256) and return its claims."""
    client = _jwks_client()
    try:
        signing_key = client.get_signing_key_from_jwt(token)
        payload: dict[str, object] = decode(
            token,
            signing_key.key,
            algorithms=["ES256"],
            audience="authenticated",
        )
    except PyJWTError as exc:
        raise ValueError(f"Invalid token: {exc}") from exc

    return TokenClaims(
        sub=str(payload["sub"]),
        email=str(payload.get("email", "")),
    )
