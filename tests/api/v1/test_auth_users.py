"""Ручки auth та users."""
import pytest
from httpx import AsyncClient

from tests.conftest import auth_headers, register


@pytest.mark.asyncio
async def test_register_login_me_cookie_and_bearer(client: AsyncClient):
    await register(client, "a@a.com", "password1")
    login = await client.post("/api/v1/auth/login", json={"email": "a@a.com", "password": "password1"})
    assert login.status_code == 200
    assert "access_token" in login.json()
    me = await client.get("/api/v1/auth/me")
    assert me.status_code == 200
    assert me.json()["email"] == "a@a.com"

    h = await auth_headers(client, "a@a.com", "password1")
    me2 = await client.get("/api/v1/auth/me", headers=h)
    assert me2.status_code == 200


@pytest.mark.asyncio
async def test_users_crud_http(client: AsyncClient):
    await register(client, "owner@test.com", "password1")
    headers = await auth_headers(client, "owner@test.com", "password1")

    lst = await client.get("/api/v1/users/", headers=headers)
    assert lst.status_code == 200
    assert len(lst.json()) >= 1

    r = await client.get("/api/v1/users/1", headers=headers)
    assert r.status_code == 200

    u = await client.post(
        "/api/v1/users/",
        json={"email": "new@test.com", "password": "password1"},
    )
    assert u.status_code == 201

    uid = u.json()["id"]
    up = await client.put(f"/api/v1/users/{uid}", headers=headers, json={"is_active": False})
    assert up.status_code == 200
    assert up.json()["is_active"] is False

    de = await client.delete(f"/api/v1/users/{uid}", headers=headers)
    assert de.status_code == 204
