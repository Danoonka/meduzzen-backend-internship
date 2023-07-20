from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from app.models.models_user import User, UserCreate, UserUpdate, UserResponseModel, UserList, UserDeleteResponse
from passlib.context import CryptContext


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_users(self, page: int = 1, page_size: int = 10):
        query = select(User).options(selectinload(User.user_links))
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_user_by_id(self, user_id: int) -> User:
        result = await self.session.execute(
            select(User).where(User.user_id == user_id).options(selectinload(User.user_links))
        )
        return result.scalar_one_or_none()

    async def create_user(self, user_data: UserCreate) -> UserResponseModel:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hashed_password = pwd_context.hash(user_data.user_password)
        user = User(
            user_email=user_data.user_email,
            user_firstname=user_data.user_firstname,
            user_lastname=user_data.user_lastname,
            user_password=hashed_password
        )
        self.session.add(user)
        await self.session.flush()
        await self.session.commit()

        return UserResponseModel(user=user)

    async def update_user(self, user_id: int, user_data: UserUpdate) -> UserResponseModel:
        user = await self.get_user_by_id(user_id=user_id)
        if user:
            for field, value in user_data.dict(exclude_unset=True).items():
                setattr(user, field, value)
            await self.session.flush()
            await self.session.commit()
            return user

    async def delete_user(self, user_id: int) -> dict[str, UserResponseModel]:
        user = await self.get_user_by_id(user_id=user_id)
        if user:
            self.session.delete(user)
            await self.session.flush()
            await self.session.commit()
        return {"message": "User deleted successfully", "user": user}
