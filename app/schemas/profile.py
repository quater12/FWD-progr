"""User profile schemas."""
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UserProfileBase(BaseModel):
    full_name: str = Field(min_length=1, max_length=255)
    phone: Optional[str] = Field(default=None, max_length=64)
    address: Optional[str] = Field(default=None, max_length=512)


class UserProfileCreate(UserProfileBase):
    user_id: int


class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    phone: Optional[str] = Field(default=None, max_length=64)
    address: Optional[str] = Field(default=None, max_length=512)


class UserProfileResponse(UserProfileBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
