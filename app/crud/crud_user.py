"""User CRUD."""
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User]):
    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        result = await db.scalars(select(User).where(User.email == email))
        return result.first()

    async def get_by_nickname(self, db: AsyncSession, nickname: str) -> Optional[User]:
        result = await db.scalars(select(User).where(User.nickname == nickname))
        return result.first()

    async def create_user(self, db: AsyncSession, obj_in: UserCreate) -> User:
        data = {
            "email": obj_in.email,
            "nickname": getattr(obj_in, "nickname", None),
            "hashed_password": hash_password(obj_in.password),
        }
        return await self.create(db, data=data)

    async def update_user(self, db: AsyncSession, *, db_user: User, obj_in: UserUpdate) -> User:
        payload = obj_in.model_dump(exclude_unset=True)
        if "password" in payload and payload["password"]:
            payload["hashed_password"] = hash_password(payload.pop("password"))
        return await self.update(db, db_obj=db_user, data=payload)


crud_user = CRUDUser(User)
