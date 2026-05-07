"""CRUD товарів."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud_product import crud_product
from app.db.session import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter()


@router.get("/", response_model=list[ProductResponse])
async def list_products(skip: int = 0, limit: int = 50, db: AsyncSession = Depends(get_db)) -> list[Product]:
    rows = await crud_product.list(db, skip=skip, limit=limit)
    return list(rows)


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(*, db: AsyncSession = Depends(get_db), body: ProductCreate) -> Product:
    return await crud_product.create_product(db, body)


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)) -> Product:
    p = await crud_product.get(db, product_id)
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    return p


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    body: ProductUpdate,
    db: AsyncSession = Depends(get_db),
) -> Product:
    p = await crud_product.get(db, product_id)
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    return await crud_product.update_product(db, db_obj=p, obj_in=body)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)) -> None:
    ok = await crud_product.delete(db, id_=product_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Product not found")
