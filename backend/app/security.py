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
    return PyJWKClient(f"{get_settings().supabase_url}/auth/v1/.well-known/jwks.json")


def verify_jwt(token: str) -> TokenClaims:
    client = _jwks_client()
    try:
        signing_key = client.get_signing_key_from_jwt(token)
        payload: dict[str, object] = decode(
            token,
            signing_key.key,
            algorithms=["RS256", "ES256"],
            audience="authenticated",
        )
    except PyJWTError as exc:
        raise ValueError(f"Invalid token: {exc}") from exc

    return TokenClaims(
        sub=str(payload["sub"]),
        email=str(payload.get("email", "")),
    )
