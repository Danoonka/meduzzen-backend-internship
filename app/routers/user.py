from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_postgres_handler import get_session
from app.models.models_user import UserCreate, UserUpdate
from app.services.user import get_all_users, get_user_by_id, create_user, update_user, delete_user

user_router = APIRouter()


@user_router.get("/")
async def get_users(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1),session: AsyncSession = Depends(get_session)):
    users = await get_all_users(session, page, page_size)
    return {"users": users}


@user_router.get("/{user_id}")
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await get_user_by_id(user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.post("/")
async def create_new_user(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    user = await create_user(user_data, session)
    return user


@user_router.put("/{user_id}")
async def update_existing_user(user_id: int, user_data: UserUpdate, session: AsyncSession = Depends(get_session)):
    user = await update_user(user_id, user_data, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.delete("/{user_id}")
async def delete_existing_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await delete_user(user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
