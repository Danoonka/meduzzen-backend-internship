from typing import List, Dict

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_postgres_handler import get_session
from app.models.models_user import UserCreate, UserUpdate, User, UserResponseModel, UserList, UserDeleteResponse
from app.services.user import UserService

user_router = APIRouter()


async def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(session)


@user_router.get("/", response_model=List[UserResponseModel])
async def get_users(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1),
                    user_service: UserService = Depends(get_user_service)) -> List[UserResponseModel]:
    users = await user_service.get_all_users(page=page, page_size=page_size)
    return users


@user_router.get("/{user_id}", response_model=UserResponseModel)
async def get_user(user_id: int, user_service: UserService = Depends(get_user_service)) -> UserResponseModel:
    user = await user_service.get_user_by_id(user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.post("/", response_model=UserResponseModel)
async def create_new_user(user_data: UserCreate,
                          user_service: UserService = Depends(get_user_service)) -> UserResponseModel:
    user = await user_service.create_user(user_data=user_data)
    return user


@user_router.put("/{user_id}", response_model=UserResponseModel)
async def update_existing_user(user_id: int, user_data: UserUpdate,
                               user_service: UserService = Depends(get_user_service)) -> UserResponseModel:
    user = await user_service.update_user(user_id=user_id, user_data=user_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.delete("/{user_id}", response_model=UserDeleteResponse)
async def delete_existing_user(user_id: int,
                               user_service: UserService = Depends(get_user_service)) -> UserDeleteResponse:
    user = await user_service.delete_user(user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
