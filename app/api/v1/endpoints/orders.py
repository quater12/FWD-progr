"""CRUD замовлень; створення з позиціями — лише для аутентифікованого користувача."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.crud.crud_order import crud_order
from app.db.session import get_db
from app.models.order import Order
from app.models.user import User
from app.schemas.order import OrderCreate, OrderResponse, OrderUpdate

router = APIRouter()


@router.get("/", response_model=list[OrderResponse])
async def list_orders(skip: int = 0, limit: int = 50, db: AsyncSession = Depends(get_db)) -> list[Order]:
    rows = await crud_order.list(db, skip=skip, limit=limit)
    out: list[Order] = []
    for r in rows:
        loaded = await crud_order.get_with_items(db, r.id)
        if loaded:
            out.append(loaded)
    return out


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    *,
    db: AsyncSession = Depends(get_db),
    body: OrderCreate,
    current: User = Depends(get_current_user),
) -> Order:
    return await crud_order.create_with_items(db, user_id=current.id, obj_in=body)


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, db: AsyncSession = Depends(get_db)) -> Order:
    o = await crud_order.get_with_items(db, order_id)
    if not o:
        raise HTTPException(status_code=404, detail="Order not found")
    return o


@router.put("/{order_id}", response_model=OrderResponse)
async def update_order(order_id: int, body: OrderUpdate, db: AsyncSession = Depends(get_db)) -> Order:
    o = await crud_order.get(db, order_id)
    if not o:
        raise HTTPException(status_code=404, detail="Order not found")
    return await crud_order.update_order(db, db_obj=o, obj_in=body)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: int, db: AsyncSession = Depends(get_db)) -> None:
    ok = await crud_order.delete_order(db, id_=order_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Order not found")
