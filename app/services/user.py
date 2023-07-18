from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.models_user import User, UserCreate, UserUpdate
from passlib.context import CryptContext


async def get_all_users(session: AsyncSession, page: int = 1, page_size: int = 10) -> List[User]:
    query = select(User).options(selectinload(User.user_links))
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)

    result = await session.execute(query)
    return result.scalars().all()


async def get_user_by_id(user_id: int, session: AsyncSession) -> User:
    result = await session.execute(select(User).where(User.user_id == user_id).options(selectinload(User.user_links)))
    return result.scalar_one_or_none()


async def create_user(user_data: UserCreate, session: AsyncSession) -> User:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(user_data.user_password)
    user = User(
        user_email=user_data.user_email,
        user_firstname=user_data.user_firstname,
        user_lastname=user_data.user_lastname,
        user_password=hashed_password
    )
    session.add(user)
    await session.flush()
    await session.commit()
    return user


async def update_user(user_id: int, user_data: UserUpdate, session: AsyncSession) -> User:
    user = await session.get(User, user_id)
    if user:
        for field, value in user_data.dict(exclude_unset=True).items():
            setattr(user, field, value)
        await session.flush()
        await session.commit()
        return user


async def delete_user(user_id: int, session: AsyncSession) -> User:
    user = await session.get(User, user_id)
    if user:
        await session.delete(user)
        await session.flush()
        await session.commit()
    return user
