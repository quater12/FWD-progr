"""OrderItem CRUD."""
from app.crud.base import CRUDBase
from app.models.order_item import OrderItem
from app.schemas.order_item import OrderItemCreate, OrderItemUpdate


class CRUDOrderItem(CRUDBase[OrderItem]):
    async def create_item(self, db, obj_in: OrderItemCreate, *, order_id: int) -> OrderItem:
        data = obj_in.model_dump()
        data["order_id"] = order_id
        return await self.create(db, data=data)

    async def update_item(self, db, *, db_obj: OrderItem, obj_in: OrderItemUpdate) -> OrderItem:
        return await self.update(db, db_obj=db_obj, data=obj_in.model_dump(exclude_unset=True))


crud_order_item = CRUDOrderItem(OrderItem)
