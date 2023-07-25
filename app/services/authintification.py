from typing import Optional
import jwt
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.models_user import User, UserResponseModel
from app.utils.utils import verify_password, verify, generate_temporary_password, get_password_hash, toUserResponse
from config import SECRET_KEY, ALGORITHM


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_username(self, username: str) -> User:
        user = await self.session.scalar(
            select(User).where(User.user_email == username).options(selectinload(User.user_links))
        )
        return user

    async def authenticate_user(self, username: str, password: str) -> UserResponseModel:
        user = await self.get_user_by_username(username=username)
        if user and verify_password(plain_password=password, hashed_password=user.user_password):
            return user

    async def create_user_from_auth0(self, token) -> UserResponseModel:
        auth0_data = verify(token=token)
        user = await self.get_user_by_username(auth0_data.get("e-mail"))
        if user:
            return user
        else:
            user_password = generate_temporary_password()
            hashed_password = await get_password_hash(password=user_password)
            user = User(
                user_email=auth0_data.get("e-mail"),
                user_firstname=auth0_data.get("e-mail"),
                user_lastname=auth0_data.get("e-mail"),
                user_password=hashed_password
            )

            self.session.add(user)
            await self.session.flush()
            await self.session.commit()

            return toUserResponse(user)

    async def get_user_from_token(self, token) -> Optional[dict]:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user = await self.get_user_by_username(payload['user_email'])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            return False
        return user
