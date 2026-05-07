"""Початкові дані: по кілька записів у кожну таблицю (лаб. 4)."""
import asyncio
from decimal import Decimal

from sqlalchemy import func, select

from app.core.security import hash_password
from app.db.session import AsyncSessionLocal
from app.models.category import Category
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.models.user import User
from app.models.user_profile import UserProfile


async def run_seed() -> None:
    async with AsyncSessionLocal() as session:
        existing = await session.scalar(select(func.count()).select_from(Category))
        if existing and existing > 0:
            return

        u1 = User(email="admin@example.com", nickname="admin", hashed_password=hash_password("adminpass"), is_active=True)
        u2 = User(email="buyer@example.com", nickname="buyer", hashed_password=hash_password("buyerpass"), is_active=True)
        session.add_all([u1, u2])
        await session.flush()

        session.add_all(
            [
                UserProfile(user_id=u1.id, full_name="Admin User", phone="+380501111111", address="Kyiv"),
                UserProfile(user_id=u2.id, full_name="Buyer User", phone="+380502222222", address="Lviv"),
            ]
        )

        c1 = Category(name="Електроніка", description="Гаджети та пристрої")
        c2 = Category(name="Книги", description="Паперові та електронні книги")
        session.add_all([c1, c2])
        await session.flush()

        p1 = Product(
            category_id=c1.id,
            name="USB Cable",
            description="Type-C cable",
            price=Decimal("9.99"),
            stock=100,
        )
        p2 = Product(
            category_id=c1.id,
            name="Mouse",
            description="Wireless mouse",
            price=Decimal("29.50"),
            stock=40,
        )
        p3 = Product(
            category_id=c2.id,
            name="Python Guide",
            description="Learning Python",
            price=Decimal("19.00"),
            stock=25,
        )
        p4 = Product(
            category_id=c2.id,
            name="SQL Cookbook",
            description="Recipes for SQL",
            price=Decimal("24.00"),
            stock=15,
        )
        session.add_all([p1, p2, p3, p4])
        await session.flush()

        o1 = Order(user_id=u2.id, status="paid", total_amount=Decimal("0.00"))
        o2 = Order(user_id=u2.id, status="pending", total_amount=Decimal("0.00"))
        session.add_all([o1, o2])
        await session.flush()

        lines = [
            OrderItem(order_id=o1.id, product_id=p1.id, quantity=2, unit_price=Decimal("9.99")),
            OrderItem(order_id=o1.id, product_id=p3.id, quantity=1, unit_price=Decimal("19.00")),
            OrderItem(order_id=o2.id, product_id=p2.id, quantity=1, unit_price=Decimal("29.50")),
            OrderItem(order_id=o2.id, product_id=p4.id, quantity=1, unit_price=Decimal("24.00")),
        ]
        session.add_all(lines)

        o1.total_amount = Decimal("9.99") * 2 + Decimal("19.00")
        o2.total_amount = Decimal("29.50") + Decimal("24.00")
        p1.stock -= 2
        p3.stock -= 1
        p2.stock -= 1
        p4.stock -= 1

        await session.commit()


def main() -> None:
    asyncio.run(run_seed())


if __name__ == "__main__":
    main()
