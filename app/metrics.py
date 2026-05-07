"""Prometheus custom metrics and refresh helpers."""
from decimal import Decimal

from prometheus_client import Gauge
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order

# Lab 7: custom business metric — сумарна вартість усіх замовлень
TOTAL_ORDERS_VALUE = Gauge(
    "ecommerce_orders_total_value",
    "Sum of Order.total_amount for all orders",
)


async def refresh_orders_total_value(db: AsyncSession) -> None:
    q = select(func.coalesce(func.sum(Order.total_amount), 0))
    total = await db.scalar(q)
    if total is None:
        TOTAL_ORDERS_VALUE.set(0.0)
    else:
        TOTAL_ORDERS_VALUE.set(float(Decimal(total)))
