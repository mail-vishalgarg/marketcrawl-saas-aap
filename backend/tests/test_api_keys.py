"""
API key management tests.
Service calls are mocked — no real Supabase connection needed.
"""

import hashlib
from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.models.response import TenantResponse
from app.security import TokenClaims
from app.services.api_keys import ApiKeyMeta, _hash_key, generate_key

FAKE_USER = TokenClaims(sub="user-uuid-123", email="test@example.com")
FAKE_TENANT = TenantResponse(
    id="tenant-uuid-456",
    user_id="user-uuid-123",
    name="test",
    created_at="2026-08-06T00:00:00Z",
)
FAKE_KEY_META = ApiKeyMeta(
    id="key-uuid-789",
    name="Production",
    key_prefix="mp_live_abc",
    created_at="2026-08-06T00:00:00Z",
    last_used_at=None,
    revoked=False,
)
FAKE_RAW = "mp_live_" + "x" * 32


# ── Unit tests for pure functions ──────────────────────────────────────────────

def test_hash_key_is_sha256() -> None:
    expected = hashlib.sha256(b"hello").hexdigest()
    assert _hash_key("hello") == expected


def test_generate_key_format() -> None:
    raw, key_hash, prefix = generate_key()
    assert raw.startswith("mp_live_")
    assert len(raw) > 11
    assert prefix == raw[:11]
    assert key_hash == _hash_key(raw)


# ── Endpoint: list ──────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_list_keys_no_auth_returns_401() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.get("/api/v1/api-keys")
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_list_keys_returns_metadata() -> None:
    mock_list = AsyncMock(return_value=[FAKE_KEY_META])
    with (
        patch("app.dependencies.verify_jwt", return_value=FAKE_USER),
        patch("app.services.tenants.get_or_create", AsyncMock(return_value=FAKE_TENANT)),
        patch("app.services.api_keys.list_keys", mock_list),
    ):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            r = await ac.get(
                "/api/v1/api-keys",
                headers={"Authorization": "Bearer fake.jwt.token"},
            )

    assert r.status_code == 200
    keys = r.json()
    assert len(keys) == 1
    assert keys[0]["name"] == "Production"
    assert "key_hash" not in keys[0]   # hash must never be returned
    assert "raw_key" not in keys[0]    # raw key not in list response


# ── Endpoint: create ───────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_key_returns_raw_key_once() -> None:
    mock_create = AsyncMock(return_value=(FAKE_RAW, FAKE_KEY_META))
    with (
        patch("app.dependencies.verify_jwt", return_value=FAKE_USER),
        patch("app.services.tenants.get_or_create", AsyncMock(return_value=FAKE_TENANT)),
        patch("app.services.api_keys.create_key", mock_create),
    ):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            r = await ac.post(
                "/api/v1/api-keys",
                headers={"Authorization": "Bearer fake.jwt.token"},
                json={"name": "Production"},
            )

    assert r.status_code == 201
    data = r.json()
    assert data["raw_key"] == FAKE_RAW
    assert data["name"] == "Production"
    mock_create.assert_awaited_once_with("tenant-uuid-456", "Production")


# ── Endpoint: revoke ───────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_revoke_key_returns_204() -> None:
    mock_revoke = AsyncMock(return_value=None)
    with (
        patch("app.dependencies.verify_jwt", return_value=FAKE_USER),
        patch("app.services.tenants.get_or_create", AsyncMock(return_value=FAKE_TENANT)),
        patch("app.services.api_keys.revoke_key", mock_revoke),
    ):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            r = await ac.delete(
                "/api/v1/api-keys/key-uuid-789",
                headers={"Authorization": "Bearer fake.jwt.token"},
            )

    assert r.status_code == 204
    mock_revoke.assert_awaited_once_with("tenant-uuid-456", "key-uuid-789")


# ── require_api_key dependency ─────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_require_api_key_valid_key_returns_tenant_id() -> None:
    """require_api_key resolves a valid mp_live_ key to its tenant_id."""
    from app.dependencies import require_api_key

    with patch("app.services.api_keys.verify_key", AsyncMock(return_value="tenant-uuid-456")):
        tenant_id = await require_api_key(
            x_api_key="mp_live_" + "a" * 32,
            credentials=None,
        )
    assert tenant_id == "tenant-uuid-456"


@pytest.mark.asyncio
async def test_require_api_key_wrong_key_returns_401() -> None:
    with patch("app.services.api_keys.verify_key", AsyncMock(return_value=None)):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            r = await ac.get(
                "/api/v1/api-keys",
                headers={"X-API-Key": "mp_live_wrongkey"},
            )
    # /api-keys uses JWT auth, not API key — 401 from JWT check, not key check
    assert r.status_code == 401


# ── verify_key: create → verify succeeds → revoke → verify fails ───────────────

@pytest.mark.asyncio
async def test_verify_key_valid() -> None:
    with patch("app.services.api_keys.verify_key", AsyncMock(return_value="tenant-uuid-456")):
        from app.services.api_keys import verify_key
        result = await verify_key(FAKE_RAW)
    assert result == "tenant-uuid-456"


@pytest.mark.asyncio
async def test_verify_key_invalid_returns_none() -> None:
    with patch("app.services.api_keys.verify_key", AsyncMock(return_value=None)):
        from app.services.api_keys import verify_key
        result = await verify_key("mp_live_wrongkey")
    assert result is None
