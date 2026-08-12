from jwt import decode
from jwt.exceptions import PyJWTError
from pydantic import BaseModel

from app.settings import get_settings


class TokenClaims(BaseModel):
    sub: str
    email: str


def verify_jwt(token: str) -> TokenClaims:
    s = get_settings()
    try:
        payload: dict[str, object] = decode(
            token,
            s.supabase_jwt_secret,
            algorithms=["HS256"],
            audience="authenticated",
        )
    except PyJWTError as exc:
        raise ValueError(f"Invalid token: {exc}") from exc

    return TokenClaims(
        sub=str(payload["sub"]),
        email=str(payload.get("email", "")),
    )
