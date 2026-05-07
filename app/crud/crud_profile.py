"""UserProfile CRUD."""
from app.crud.base import CRUDBase
from app.models.user_profile import UserProfile
from app.schemas.profile import UserProfileCreate, UserProfileUpdate


class CRUDProfile(CRUDBase[UserProfile]):
    async def create_profile(self, db, obj_in: UserProfileCreate) -> UserProfile:
        data = obj_in.model_dump()
        return await self.create(db, data=data)

    async def update_profile(self, db, *, db_obj: UserProfile, obj_in: UserProfileUpdate) -> UserProfile:
        data = obj_in.model_dump(exclude_unset=True)
        return await self.update(db, db_obj=db_obj, data=data)


crud_profile = CRUDProfile(UserProfile)
