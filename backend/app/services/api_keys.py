import hashlib
import hmac
import secrets
from datetime import UTC, datetime

import httpx
from pydantic import BaseModel

from app.settings import get_settings


class ApiKeyMeta(BaseModel):
    id: str
    name: str
    key_prefix: str
    created_at: str
    last_used_at: str | None
    revoked: bool


def _hash_key(raw_key: str) -> str:
    return hashlib.sha256(raw_key.encode()).hexdigest()


def _headers() -> dict[str, str]:
    s = get_settings()
    return {
        "apikey": s.supabase_service_role_key,
        "Authorization": f"Bearer {s.supabase_service_role_key}",
        "Content-Type": "application/json",
    }


def generate_key() -> tuple[str, str, str]:
    """Return (raw_key, key_hash, key_prefix)."""
    raw = "mp_live_" + secrets.token_urlsafe(32)
    return raw, _hash_key(raw), raw[:11]


async def create_key(tenant_id: str, name: str) -> tuple[str, ApiKeyMeta]:
    """Insert a new API key row. Returns (raw_key, metadata)."""
    s = get_settings()
    raw, key_hash, prefix = generate_key()

    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{s.supabase_url}/rest/v1/api_keys",
            json={
                "tenant_id": tenant_id,
                "name": name,
                "key_prefix": prefix,
                "key_hash": key_hash,
            },
            headers={**_headers(), "Prefer": "return=representation"},
        )
        r.raise_for_status()
        row = r.json()[0]

    return raw, ApiKeyMeta.model_validate(row)


async def list_keys(tenant_id: str) -> list[ApiKeyMeta]:
    s = get_settings()
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{s.supabase_url}/rest/v1/api_keys",
            params={
                "tenant_id": f"eq.{tenant_id}",
                "select": "id,name,key_prefix,created_at,last_used_at,revoked",
                "order": "created_at.desc",
            },
            headers=_headers(),
        )
        r.raise_for_status()

    return [ApiKeyMeta.model_validate(row) for row in r.json()]


async def revoke_key(tenant_id: str, key_id: str) -> None:
    s = get_settings()
    async with httpx.AsyncClient() as client:
        r = await client.patch(
            f"{s.supabase_url}/rest/v1/api_keys",
            params={"id": f"eq.{key_id}", "tenant_id": f"eq.{tenant_id}"},
            json={"revoked": True},
            headers=_headers(),
        )
        r.raise_for_status()


async def verify_key(raw_key: str) -> str | None:
    """Hash the incoming key, look up a non-revoked row, update last_used_at.
    Returns tenant_id if valid, None otherwise."""
    s = get_settings()
    computed_hash = _hash_key(raw_key)

    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{s.supabase_url}/rest/v1/api_keys",
            params={
                "key_hash": f"eq.{computed_hash}",
                "revoked": "eq.false",
                "select": "id,tenant_id,key_hash",
                "limit": "1",
            },
            headers=_headers(),
        )
        r.raise_for_status()
        rows: list[dict[str, object]] = r.json()

        if not rows:
            return None

        row = rows[0]
        stored_hash = str(row["key_hash"])

        # constant-time comparison to prevent timing attacks
        if not hmac.compare_digest(stored_hash, computed_hash):
            return None

        await client.patch(
            f"{s.supabase_url}/rest/v1/api_keys",
            params={"id": f"eq.{row['id']}"},
            json={"last_used_at": datetime.now(UTC).isoformat()},
            headers=_headers(),
        )

    return str(row["tenant_id"])
