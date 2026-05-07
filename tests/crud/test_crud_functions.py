"""Прямі виклики функцій CRUD (шар роботи з БД)."""
from decimal import Decimal

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud_category import crud_category
from app.crud.crud_order import crud_order
from app.crud.crud_product import crud_product
from app.crud.crud_profile import crud_profile
from app.crud.crud_user import crud_user
from app.schemas.category import CategoryCreate
from app.schemas.order import OrderCreate, OrderItemLineIn, OrderUpdate
from app.schemas.product import ProductCreate, ProductUpdate
from app.schemas.profile import UserProfileCreate, UserProfileUpdate
from app.schemas.user import UserCreate, UserUpdate


@pytest.mark.asyncio
async def test_crud_user_profile_category_product(db_session: AsyncSession):
    u = await crud_user.create_user(db_session, UserCreate(email="c@test.com", password="secret12"))
    assert u.id is not None
    assert await crud_user.get(db_session, u.id) is not None
    assert await crud_user.get_by_email(db_session, "c@test.com") is not None

    await crud_user.update_user(db_session, db_user=u, obj_in=UserUpdate(is_active=False))
    assert (await crud_user.get(db_session, u.id)).is_active is False

    prof = await crud_profile.create_profile(
        db_session,
        UserProfileCreate(user_id=u.id, full_name="N", phone=None, address=None),
    )
    await crud_profile.update_profile(
        db_session, db_obj=prof, obj_in=UserProfileUpdate(full_name="N3")
    )

    cat = await crud_category.create_category(db_session, CategoryCreate(name="C1", description=""))
    pr = await crud_product.create_product(
        db_session,
        ProductCreate(name="P", description="", price="1.00", stock=5, category_id=cat.id),
    )
    await crud_product.update_product(db_session, db_obj=pr, obj_in=ProductUpdate(stock=3))

    assert await crud_product.delete(db_session, id_=pr.id)
    assert await crud_category.delete(db_session, id_=cat.id)
    assert await crud_profile.delete(db_session, id_=prof.id)
    assert await crud_user.delete(db_session, id_=u.id)


@pytest.mark.asyncio
async def test_crud_order_with_items(db_session: AsyncSession):
    u = await crud_user.create_user(db_session, UserCreate(email="o@test.com", password="secret12"))
    cat = await crud_category.create_category(db_session, CategoryCreate(name="OC", description=""))
    pr = await crud_product.create_product(
        db_session,
        ProductCreate(name="OP", description="", price="3.00", stock=5, category_id=cat.id),
    )
    order = await crud_order.create_with_items(
        db_session,
        user_id=u.id,
        obj_in=OrderCreate(
            status="pending",
            items=[OrderItemLineIn(product_id=pr.id, quantity=2)],
        ),
    )
    assert order.total_amount == Decimal("6.00")

    loaded = await crud_order.get_with_items(db_session, order.id)
    assert loaded is not None and len(loaded.items) == 1

    await crud_order.update_order(db_session, db_obj=loaded, obj_in=OrderUpdate(status="paid"))

    assert await crud_order.delete_order(db_session, id_=order.id)
    assert await crud_product.delete(db_session, id_=pr.id)
    assert await crud_category.delete(db_session, id_=cat.id)
    assert await crud_user.delete(db_session, id_=u.id)
