"""API v1 aggregate router."""
from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    categories,
    order_items,
    orders,
    products,
    profiles,
    users,
)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(profiles.router, prefix="/profiles", tags=["profiles"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(order_items.router, prefix="/order-items", tags=["order-items"])
