"""Order CRUD and order-with-lines creation."""
from decimal import Decimal
from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.metrics import refresh_orders_total_value
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.schemas.order import OrderCreate, OrderUpdate


class CRUDOrder(CRUDBase[Order]):
    async def get_with_items(self, db: AsyncSession, id_: int) -> Order | None:
        q = select(Order).options(selectinload(Order.items)).where(Order.id == id_)
        return (await db.scalars(q)).first()

    async def list_for_user(self, db: AsyncSession, user_id: int) -> Sequence[Order]:
        q = (
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.user_id == user_id)
            .order_by(Order.id.desc())
        )
        return (await db.scalars(q)).all()

    async def create_with_items(
        self,
        db: AsyncSession,
        *,
        user_id: int,
        obj_in: OrderCreate,
    ) -> Order:
        total = Decimal("0.00")
        pending_lines: list[dict] = []

        for line in obj_in.items:
            product = await db.get(Product, line.product_id)
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Product {line.product_id} not found",
                )
            if product.stock < line.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock for product {product.id}",
                )
            unit_price = Decimal(product.price)
            line_total = unit_price * line.quantity
            total += line_total
            pending_lines.append(
                {
                    "product": product,
                    "quantity": line.quantity,
                    "unit_price": unit_price,
                }
            )

        order = Order(user_id=user_id, status=obj_in.status, total_amount=total)
        db.add(order)
        await db.flush()

        for pl in pending_lines:
            p: Product = pl["product"]
            p.stock -= pl["quantity"]
            db.add(
                OrderItem(
                    order_id=order.id,
                    product_id=p.id,
                    quantity=pl["quantity"],
                    unit_price=pl["unit_price"],
                )
            )

        await db.commit()
        await db.refresh(order)
        loaded = await self.get_with_items(db, order.id)
        assert loaded is not None
        await refresh_orders_total_value(db)
        return loaded

    async def update_order(self, db: AsyncSession, *, db_obj: Order, obj_in: OrderUpdate) -> Order:
        updated = await self.update(db, db_obj=db_obj, data=obj_in.model_dump(exclude_unset=True))
        await refresh_orders_total_value(db)
        return updated

    async def delete_order(self, db: AsyncSession, *, id_: int) -> bool:
        ok = await self.delete(db, id_=id_)
        if ok:
            await refresh_orders_total_value(db)
        return ok

    async def recalculate_total(self, db: AsyncSession, order_id: int) -> Order | None:
        order = await self.get_with_items(db, order_id)
        if not order:
            return None
        total = sum((Decimal(i.unit_price) * i.quantity for i in order.items), Decimal("0"))
        order.total_amount = total
        db.add(order)
        await db.commit()
        await db.refresh(order)
        await refresh_orders_total_value(db)
        return order


crud_order = CRUDOrder(Order)
