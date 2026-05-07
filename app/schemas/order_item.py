"""Order line item schemas."""
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(ge=1)
    unit_price: Optional[Decimal] = Field(default=None, ge=0)


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemUpdate(BaseModel):
    product_id: Optional[int] = None
    quantity: Optional[int] = Field(default=None, ge=1)
    unit_price: Optional[Decimal] = Field(default=None, ge=0)


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int
    product_id: int
    quantity: int
    unit_price: Decimal
