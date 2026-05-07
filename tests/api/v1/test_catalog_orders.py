"""Каталог, замовлення, позиції, профілі — повний набір HTTP методів."""
from decimal import Decimal

import pytest
from httpx import AsyncClient

from tests.conftest import auth_headers, register


@pytest.mark.asyncio
async def test_categories_products_profiles_crud(client: AsyncClient):
    c = await client.post("/api/v1/categories/", json={"name": "Cat A", "description": "d"})
    assert c.status_code == 201
    cid = c.json()["id"]

    g = await client.get(f"/api/v1/categories/{cid}")
    assert g.status_code == 200

    u = await client.put(f"/api/v1/categories/{cid}", json={"name": "Cat B"})
    assert u.status_code == 200

    p = await client.post(
        "/api/v1/products/",
        json={
            "name": "P1",
            "description": "",
            "price": "10.00",
            "stock": 5,
            "category_id": cid,
        },
    )
    assert p.status_code == 201
    pid = p.json()["id"]

    pl = await client.get("/api/v1/products/")
    assert pl.status_code == 200

    pu = await client.put(f"/api/v1/products/{pid}", json={"stock": 3})
    assert pu.status_code == 200

    await register(client, "prof@test.com", "password1")
    pr = await client.post(
        "/api/v1/profiles/",
        json={"user_id": 1, "full_name": "FN", "phone": None, "address": None},
    )
    assert pr.status_code == 201
    prid = pr.json()["id"]

    prg = await client.get(f"/api/v1/profiles/{prid}")
    assert prg.status_code == 200

    pru = await client.put(f"/api/v1/profiles/{prid}", json={"full_name": "FN2"})
    assert pru.status_code == 200

    prd = await client.delete(f"/api/v1/profiles/{prid}")
    assert prd.status_code == 204

    dpr = await client.delete(f"/api/v1/products/{pid}")
    assert dpr.status_code == 204

    dc = await client.delete(f"/api/v1/categories/{cid}")
    assert dc.status_code == 204


@pytest.mark.asyncio
async def test_orders_flow(client: AsyncClient):
    c = await client.post("/api/v1/categories/", json={"name": "OCat", "description": ""})
    cid = c.json()["id"]
    p = await client.post(
        "/api/v1/products/",
        json={"name": "Item", "description": "", "price": "2.00", "stock": 10, "category_id": cid},
    )
    pid = p.json()["id"]

    await register(client, "buyer@test.com", "password1")
    headers = await auth_headers(client, "buyer@test.com", "password1")

    o = await client.post(
        "/api/v1/orders/",
        headers=headers,
        json={"status": "pending", "items": [{"product_id": pid, "quantity": 2}]},
    )
    assert o.status_code == 201
    oid = o.json()["id"]
    assert Decimal(o.json()["total_amount"]) == Decimal("4.00")

    og = await client.get(f"/api/v1/orders/{oid}")
    assert og.status_code == 200

    ol = await client.get("/api/v1/orders/")
    assert ol.status_code == 200

    ou = await client.put(f"/api/v1/orders/{oid}", json={"status": "paid"})
    assert ou.status_code == 200

    it = await client.post(
        f"/api/v1/order-items/?order_id={oid}",
        json={"product_id": pid, "quantity": 1, "unit_price": None},
    )
    assert it.status_code == 201
    iid = it.json()["id"]

    ig = await client.get(f"/api/v1/order-items/{iid}")
    assert ig.status_code == 200

    iu = await client.put(f"/api/v1/order-items/{iid}", json={"quantity": 1})
    assert iu.status_code == 200

    ide = await client.delete(f"/api/v1/order-items/{iid}")
    assert ide.status_code == 204

    ode = await client.delete(f"/api/v1/orders/{oid}")
    assert ode.status_code == 204

    dp = await client.delete(f"/api/v1/products/{pid}")
    assert dp.status_code == 204
    dc = await client.delete(f"/api/v1/categories/{cid}")
    assert dc.status_code == 204
