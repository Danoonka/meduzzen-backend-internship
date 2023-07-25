from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.models_user import User, UserCreate, UserUpdate, UserResponseModel, UserBase, UserSignUpRequest, \
    GetAllUsers
from app.utils.utils import get_password_hash


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_users(self, page: int = 1, page_size: int = 10) -> GetAllUsers:
        query = select(User).options(selectinload(User.user_links))
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        result = await self.session.execute(query)
        users = result.scalars().all()

        total_users = await self.session.scalar(select(func.count()).select_from(User))
        user_base_models = [
            UserBase(
                user_id=user.user_id,
                user_email=user.user_email,
                user_firstname=user.user_firstname,
                user_lastname=user.user_lastname,
                user_avatar=user.user_avatar
            ) for user in users
        ]
        return GetAllUsers(
            user_list=user_base_models,
            total_users=total_users
        )

    async def get_user_by_id(self, user_id: int) -> User:
        user = await self.session.scalar(
            select(User).where(User.user_id == user_id).options(selectinload(User.user_links))
        )
        return user

    async def create_user(self, user_data: UserSignUpRequest) -> UserResponseModel:
        hashed_password = await get_password_hash(password=user_data.user_password)
        user = User(
            user_email=user_data.user_email,
            user_firstname=user_data.user_firstname,
            user_lastname=user_data.user_lastname,
            user_password=hashed_password
        )
        self.session.add(user)
        await self.session.flush()
        await self.session.commit()

        return UserResponseModel(
            user_id=user.user_id,
            user_email=user.user_email,
            user_firstname=user.user_firstname,
            user_lastname=user.user_lastname,
            user_password=user.user_password
        )

    async def update_user(self, user_id: int, user_data: UserUpdate) -> UserResponseModel:
        user = await self.get_user_by_id(user_id=user_id)
        if user:
            for field, value in user_data.dict(exclude_unset=True).items():
                setattr(user, field, value)
            await self.session.flush()
            await self.session.commit()
            return user

    async def delete_user(self, user_id: int) -> int:
        user = await self.get_user_by_id(user_id=user_id)
        if user:
            await self.session.delete(user)
            await self.session.flush()
            await self.session.commit()
        return user.user_id
