"""Реєстрація, логін (JWT + cookie), поточний користувач."""
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.config import settings
from app.core.security import create_access_token, hash_password, verify_password
from app.crud.crud_user import crud_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.token import LoginRequest, Token
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(*, db: AsyncSession = Depends(get_db), body: UserCreate) -> User:
    if await crud_user.get_by_email(db, body.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    if body.nickname and await crud_user.get_by_nickname(db, body.nickname):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nickname already taken")
    return await crud_user.create_user(db, body)


@router.post("/login", response_model=Token)
async def login(
    response: Response,
    *,
    db: AsyncSession = Depends(get_db),
    body: LoginRequest,
) -> Token:
    user = await crud_user.get_by_email(db, body.email)
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access = create_access_token(user.email)
    response.set_cookie(
        key="access_token",
        value=access,
        httponly=True,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        secure=False,
    )
    return Token(access_token=access)


@router.post("/logout")
async def logout(response: Response) -> dict[str, str]:
    response.delete_cookie("access_token")
    return {"detail": "logged out"}


@router.get("/me", response_model=UserResponse)
async def read_me(current: User = Depends(get_current_user)) -> User:
    return current


@router.post("/change-password")
async def change_password(
    *,
    db: AsyncSession = Depends(get_db),
    current: User = Depends(get_current_user),
    body: dict,
) -> dict[str, str]:
    current_password = str(body.get("current_password", ""))
    new_password = str(body.get("new_password", ""))
    if len(new_password) < 6:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password too short")
    if not verify_password(current_password, current.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password incorrect")
    current.hashed_password = hash_password(new_password)
    db.add(current)
    await db.commit()
    return {"detail": "password changed"}


@router.post("/set-nickname")
async def set_nickname(
    *,
    db: AsyncSession = Depends(get_db),
    current: User = Depends(get_current_user),
    body: dict,
) -> dict[str, str]:
    nickname = str(body.get("nickname", "")).strip()
    if len(nickname) < 2 or len(nickname) > 64:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid nickname length")
    existing = await crud_user.get_by_nickname(db, nickname)
    if existing and existing.id != current.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nickname already taken")
    current.nickname = nickname
    db.add(current)
    await db.commit()
    return {"detail": "nickname updated"}
