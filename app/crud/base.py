"""Generic async CRUD base."""
from typing import Any, Generic, Optional, Sequence, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

ModelT = TypeVar("ModelT")


class CRUDBase(Generic[ModelT]):
    def __init__(self, model: Type[ModelT]) -> None:
        self.model = model

    async def get(self, db: AsyncSession, id_: int) -> Optional[ModelT]:
        return await db.get(self.model, id_)

    async def list(self, db: AsyncSession, *, skip: int = 0, limit: int = 100) -> Sequence[ModelT]:
        result = await db.scalars(select(self.model).offset(skip).limit(limit))
        return result.all()

    async def create(self, db: AsyncSession, *, data: dict[str, Any]) -> ModelT:
        obj = self.model(**data)
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def update(self, db: AsyncSession, *, db_obj: ModelT, data: dict[str, Any]) -> ModelT:
        for key, value in data.items():
            if value is not None:
                setattr(db_obj, key, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, *, id_: int) -> bool:
        obj = await db.get(self.model, id_)
        if not obj:
            return False
        await db.delete(obj)
        await db.commit()
        return True
