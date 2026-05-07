"""CRUD позицій замовлення; перерахунок total_amount замовлення."""
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud_order import crud_order
from app.crud.crud_order_item import crud_order_item
from app.db.session import get_db
from app.models.order_item import OrderItem
from app.models.product import Product
from app.schemas.order_item import OrderItemCreate, OrderItemResponse, OrderItemUpdate

router = APIRouter()


@router.get("/", response_model=list[OrderItemResponse])
async def list_items(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)) -> list[OrderItem]:
    rows = await crud_order_item.list(db, skip=skip, limit=limit)
    return list(rows)


@router.post("/", response_model=OrderItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    *,
    db: AsyncSession = Depends(get_db),
    order_id: int = Query(..., description="ID замовлення"),
    body: OrderItemCreate,
) -> OrderItem:
    parent = await crud_order.get(db, order_id)
    if not parent:
        raise HTTPException(status_code=404, detail="Order not found")
    product = await db.get(Product, body.product_id)
    if not product:
        raise HTTPException(status_code=400, detail="Product not found")
    if product.stock < body.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    unit_price = body.unit_price if body.unit_price is not None else Decimal(product.price)
    product.stock -= body.quantity
    db.add(product)
    item = await crud_order_item.create(
        db,
        data={
            "order_id": order_id,
            "product_id": body.product_id,
            "quantity": body.quantity,
            "unit_price": unit_price,
        },
    )
    await crud_order.recalculate_total(db, order_id)
    return item


@router.get("/{item_id}", response_model=OrderItemResponse)
async def get_item(item_id: int, db: AsyncSession = Depends(get_db)) -> OrderItem:
    it = await crud_order_item.get(db, item_id)
    if not it:
        raise HTTPException(status_code=404, detail="Order item not found")
    return it


@router.put("/{item_id}", response_model=OrderItemResponse)
async def update_item(
    item_id: int,
    body: OrderItemUpdate,
    db: AsyncSession = Depends(get_db),
) -> OrderItem:
    it = await crud_order_item.get(db, item_id)
    if not it:
        raise HTTPException(status_code=404, detail="Order item not found")
    oid = it.order_id
    updated = await crud_order_item.update_item(db, db_obj=it, obj_in=body)
    await crud_order.recalculate_total(db, oid)
    return updated


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)) -> None:
    it = await crud_order_item.get(db, item_id)
    if not it:
        raise HTTPException(status_code=404, detail="Order item not found")
    oid = it.order_id
    ok = await crud_order_item.delete(db, id_=item_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Order item not found")
    await crud_order.recalculate_total(db, oid)
