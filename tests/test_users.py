import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_protected_route_unauthenticated(async_client: AsyncClient):
    response = await async_client.get("/api/v1/auth/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_protected_route_authenticated(async_client: AsyncClient):
    email = "protected@example.com"
    password = "password123"

    # Signup & Login
    await async_client.post("/api/v1/auth/signup", json={
        "email": email,
        "full_name": "Protected User",
        "password": password
    })
    login_res = await async_client.post("/api/v1/auth/login", json={
        "email": email,
        "password": password
    })

    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Fetch profile
    me_res = await async_client.get("/api/v1/auth/me", headers=headers)
    assert me_res.status_code == 200
    assert me_res.json()["email"] == email

    # Fetch dashboard secret payload
    payload_res = await async_client.get("/api/v1/dashboard/secret-payload", headers=headers)
    assert payload_res.status_code == 200
    assert "Access Granted" in payload_res.json()["message"]
