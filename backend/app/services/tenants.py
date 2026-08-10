from pydantic import BaseModel

import httpx

from app.models.response import TenantResponse
from app.settings import get_settings


class _TenantRow(BaseModel):
    id: str
    user_id: str
    name: str
    created_at: str


def _headers() -> dict[str, str]:
    s = get_settings()
    return {
        "apikey": s.supabase_service_role_key,
        "Authorization": f"Bearer {s.supabase_service_role_key}",
        "Content-Type": "application/json",
    }


async def get_or_create(user_id: str, email: str) -> TenantResponse:
    """Load the tenant for this user, creating one on first login."""
    s = get_settings()
    base = f"{s.supabase_url}/rest/v1"
    hdrs = _headers()

    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{base}/tenants",
            params={"user_id": f"eq.{user_id}", "select": "*", "limit": "1"},
            headers=hdrs,
        )
        r.raise_for_status()
        rows: list[dict[str, object]] = r.json()

        if rows:
            row = _TenantRow.model_validate(rows[0])
            return TenantResponse(
                id=row.id, user_id=row.user_id, name=row.name, created_at=row.created_at
            )

        name = email.split("@")[0] if "@" in email else email
        r = await client.post(
            f"{base}/tenants",
            json={"user_id": user_id, "name": name},
            headers={**hdrs, "Prefer": "return=representation"},
        )
        r.raise_for_status()
        rows = r.json()
        row = _TenantRow.model_validate(rows[0])
        return TenantResponse(
            id=row.id, user_id=row.user_id, name=row.name, created_at=row.created_at
        )
