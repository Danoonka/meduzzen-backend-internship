from datetime import datetime
import jwt
from jose import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.models_user import User, UserCreate, UserUpdate, UserResponseModel, UserList, UserDeleteResponse
from app.services.utils import get_password_hash, verify_password
from config import SECRET_KEY, ALGORITHM


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_username(self, username: str):
        user = await self.session.execute(
            select(User).where(User.user_email == username).options(selectinload(User.user_links))
        )
        await self.session.flush()
        await self.session.commit()
        return user

    async def get_all_users(self, page: int = 1, page_size: int = 10) -> UserList:
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
            self.session.delete(user)
            await self.session.flush()
            await self.session.commit()
        return {"message": "User deleted successfully", "user": user}
        return user

    async def authenticate_user(self, username: str, password: str):
        user = self.get_user_by_username(username)
        if user and verify_password(password, user["hashed_password"]):
            return user

    def get_user_from_token(self, token: str) -> str:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            expiration = datetime.fromtimestamp(payload["exp"])
            if datetime.utcnow() >= expiration:
                return None
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
