"""CRUD профілів (one-to-one з User)."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud_profile import crud_profile
from app.db.session import get_db
from app.models.user_profile import UserProfile
from app.schemas.profile import UserProfileCreate, UserProfileResponse, UserProfileUpdate

router = APIRouter()


@router.get("/", response_model=list[UserProfileResponse])
async def list_profiles(skip: int = 0, limit: int = 50, db: AsyncSession = Depends(get_db)) -> list[UserProfile]:
    rows = await crud_profile.list(db, skip=skip, limit=limit)
    return list(rows)


@router.post("/", response_model=UserProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(*, db: AsyncSession = Depends(get_db), body: UserProfileCreate) -> UserProfile:
    return await crud_profile.create_profile(db, body)


@router.get("/{profile_id}", response_model=UserProfileResponse)
async def get_profile(profile_id: int, db: AsyncSession = Depends(get_db)) -> UserProfile:
    p = await crud_profile.get(db, profile_id)
    if not p:
        raise HTTPException(status_code=404, detail="Profile not found")
    return p


@router.put("/{profile_id}", response_model=UserProfileResponse)
async def update_profile(
    profile_id: int,
    body: UserProfileUpdate,
    db: AsyncSession = Depends(get_db),
) -> UserProfile:
    p = await crud_profile.get(db, profile_id)
    if not p:
        raise HTTPException(status_code=404, detail="Profile not found")
    return await crud_profile.update_profile(db, db_obj=p, obj_in=body)


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(profile_id: int, db: AsyncSession = Depends(get_db)) -> None:
    ok = await crud_profile.delete(db, id_=profile_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Profile not found")
