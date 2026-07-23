import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_signup_user_success(async_client: AsyncClient):
    payload = {
        "email": "testuser@example.com",
        "full_name": "Test User",
        "password": "strongpassword123"
    }
    response = await async_client.post("/api/v1/auth/signup", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert data["full_name"] == "Test User"
    assert "id" in data
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test_signup_duplicate_email_fails(async_client: AsyncClient):
    payload = {
        "email": "duplicate@example.com",
        "full_name": "Duplicate User",
        "password": "password123"
    }
    # First signup
    res1 = await async_client.post("/api/v1/auth/signup", json=payload)
    assert res1.status_code == 201

    # Second signup with same email
    res2 = await async_client.post("/api/v1/auth/signup", json=payload)
    assert res2.status_code == 400
    assert "already exists" in res2.json()["detail"]


@pytest.mark.asyncio
async def test_login_success(async_client: AsyncClient):
    email = "logintest@example.com"
    password = "secretpassword"

    # Create user first
    await async_client.post("/api/v1/auth/signup", json={
        "email": email,
        "full_name": "Login Test",
        "password": password
    })

    # Login
    response = await async_client.post("/api/v1/auth/login", json={
        "email": email,
        "password": password
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_password(async_client: AsyncClient):
    email = "invalidpass@example.com"
    await async_client.post("/api/v1/auth/signup", json={
        "email": email,
        "full_name": "User",
        "password": "correctpassword"
    })

    response = await async_client.post("/api/v1/auth/login", json={
        "email": email,
        "password": "wrongpassword"
    })

    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]
