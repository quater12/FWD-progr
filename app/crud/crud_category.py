"""Category CRUD."""
from app.crud.base import CRUDBase
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


class CRUDCategory(CRUDBase[Category]):
    async def create_category(self, db, obj_in: CategoryCreate) -> Category:
        return await self.create(db, data=obj_in.model_dump())

    async def update_category(self, db, *, db_obj: Category, obj_in: CategoryUpdate) -> Category:
        return await self.update(db, db_obj=db_obj, data=obj_in.model_dump(exclude_unset=True))


crud_category = CRUDCategory(Category)
