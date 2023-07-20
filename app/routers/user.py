from datetime import timedelta
from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.db.db_postgres_handler import get_session
from app.models.models_user import UserCreate, UserUpdate, UserResponseModel, UserSignInRequest, UserSignInResponse, \
    DeleteUserResponse
from app.services.user import UserService
from app.services.utils import create_access_token
from config import ACCESS_TOKEN_EXPIRE_MINUTES

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


@user_router.delete("/{user_id}", response_model=DeleteUserResponse)
async def delete_existing_user(user_id: int,
                               user_service: UserService = Depends(get_user_service)) -> DeleteUserResponse:
    user = await user_service.delete_user(user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "status_code": 200,
        "detail": "User delete successfully",
        "result": {
            "user_id": user
        }
    }


@user_router.post('/sign_in', response_model=UserSignInResponse)
async def authorize(data: UserSignInRequest,
                    user_service: UserService = Depends(get_user_service)) -> UserSignInResponse:
    user = user_service.authenticate_user(data.user_email, data.user_password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": data.user_email},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
