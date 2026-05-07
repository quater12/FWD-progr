"""Order schemas."""
from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.order_item import OrderItemResponse


class OrderItemLineIn(BaseModel):
    product_id: int
    quantity: int = Field(ge=1)


class OrderBase(BaseModel):
    status: str = Field(default="pending", max_length=64)


class OrderCreate(OrderBase):
    items: List[OrderItemLineIn] = Field(min_length=1)


class OrderUpdate(BaseModel):
    status: Optional[str] = Field(default=None, max_length=64)
    total_amount: Optional[Decimal] = Field(default=None, ge=0)


class OrderResponse(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    total_amount: Decimal
    created_at: datetime
    items: List[OrderItemResponse] = []
