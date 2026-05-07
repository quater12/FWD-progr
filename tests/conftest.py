"""Pytest: окрема тестова PostgreSQL (DATABASE_URL = TEST_DATABASE_URL)."""
import os

os.environ.setdefault(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://postgres:password@localhost:5432/fastapi_test",
)
os.environ["DATABASE_URL"] = os.environ["TEST_DATABASE_URL"]
os.environ.setdefault("SECRET_KEY", "test-secret-key")

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text

from app.db.session import AsyncSessionLocal, get_db
from app.main import app

TRUNCATE_SQL = (
    "TRUNCATE order_items, orders, products, categories, user_profiles, users "
    "RESTART IDENTITY CASCADE"
)


@pytest_asyncio.fixture
async def db_session():
    async with AsyncSessionLocal() as session:
        await session.execute(text(TRUNCATE_SQL))
        await session.commit()
        yield session


@pytest_asyncio.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


async def register(client: AsyncClient, email: str = "user@test.com", password: str = "secret12") -> None:
    r = await client.post("/api/v1/auth/register", json={"email": email, "password": password})
    assert r.status_code == 201, r.text


async def auth_headers(client: AsyncClient, email: str, password: str) -> dict[str, str]:
    r = await client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200, r.text
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
