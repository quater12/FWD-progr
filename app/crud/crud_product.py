"""Product CRUD."""
from app.crud.base import CRUDBase
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class CRUDProduct(CRUDBase[Product]):
    async def create_product(self, db, obj_in: ProductCreate) -> Product:
        data = obj_in.model_dump()
        return await self.create(db, data=data)

    async def update_product(self, db, *, db_obj: Product, obj_in: ProductUpdate) -> Product:
        return await self.update(db, db_obj=db_obj, data=obj_in.model_dump(exclude_unset=True))


crud_product = CRUDProduct(Product)
