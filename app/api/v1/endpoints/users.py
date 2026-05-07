"""CRUD користувачів."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.crud.crud_user import crud_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate

router = APIRouter()


@router.get("/", response_model=list[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[User]:
    rows = await crud_user.list(db, skip=skip, limit=limit)
    return list(rows)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(*, db: AsyncSession = Depends(get_db), body: UserCreate) -> User:
    if await crud_user.get_by_email(db, body.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud_user.create_user(db, body)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
) -> User:
    u = await crud_user.get(db, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    return u


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    body: UserUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
) -> User:
    u = await crud_user.get(db, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    return await crud_user.update_user(db, db_user=u, obj_in=body)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
) -> None:
    ok = await crud_user.delete(db, id_=user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
