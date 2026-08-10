"""
Auth middleware tests.
These tests mock verify_jwt and the tenant service so they don't need
real Supabase credentials.
"""

from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.models.response import TenantResponse
from app.security import TokenClaims

FAKE_USER = TokenClaims(sub="user-uuid-123", email="test@example.com")
FAKE_TENANT = TenantResponse(
    id="tenant-uuid-456",
    user_id="user-uuid-123",
    name="test",
    created_at="2026-08-06T00:00:00Z",
)


@pytest.mark.asyncio
async def test_analyze_no_token_returns_401() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.post("/api/v1/agent/analyze", json={"question": "test query"})
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_analyze_invalid_token_returns_401() -> None:
    with patch("app.dependencies.verify_jwt", side_effect=ValueError("bad token")):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            r = await ac.post(
                "/api/v1/agent/analyze",
                headers={"Authorization": "Bearer not.a.valid.jwt"},
                json={"question": "test query"},
            )
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_get_tenant_no_token_returns_401() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.get("/api/v1/me/tenant")
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_get_tenant_with_valid_token_returns_tenant() -> None:
    mock_get_or_create = AsyncMock(return_value=FAKE_TENANT)
    with (
        patch("app.dependencies.verify_jwt", return_value=FAKE_USER),
        patch("app.services.tenants.get_or_create", mock_get_or_create),
    ):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            r = await ac.get(
                "/api/v1/me/tenant",
                headers={"Authorization": "Bearer fake.valid.token"},
            )

    assert r.status_code == 200
    data = r.json()
    assert data["user_id"] == "user-uuid-123"
    assert data["name"] == "test"
    assert data["id"] == "tenant-uuid-456"
    mock_get_or_create.assert_awaited_once_with(user_id="user-uuid-123", email="test@example.com")
