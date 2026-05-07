"""CRUD категорій."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud_category import crud_category
from app.db.session import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate

router = APIRouter()


@router.get("/", response_model=list[CategoryResponse])
async def list_categories(skip: int = 0, limit: int = 50, db: AsyncSession = Depends(get_db)) -> list[Category]:
    rows = await crud_category.list(db, skip=skip, limit=limit)
    return list(rows)


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(*, db: AsyncSession = Depends(get_db), body: CategoryCreate) -> Category:
    return await crud_category.create_category(db, body)


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)) -> Category:
    c = await crud_category.get(db, category_id)
    if not c:
        raise HTTPException(status_code=404, detail="Category not found")
    return c


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    body: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
) -> Category:
    c = await crud_category.get(db, category_id)
    if not c:
        raise HTTPException(status_code=404, detail="Category not found")
    return await crud_category.update_category(db, db_obj=c, obj_in=body)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)) -> None:
    ok = await crud_category.delete(db, id_=category_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Category not found")
