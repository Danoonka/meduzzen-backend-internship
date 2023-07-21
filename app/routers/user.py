from math import ceil
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db_postgres_handler import get_session
from app.models.models_user import UserCreate, UserUpdate, UserResponseModel, DeleteUserResponse, \
    FullUserResponse, UserList, Pagination, FullUserListResponse
from app.services.user import UserService

user_router = APIRouter()


async def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(session)


@user_router.get("/", response_model=FullUserListResponse)
async def get_users(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1),
                    user_service: UserService = Depends(get_user_service)) -> FullUserListResponse:
    users, total_users = await user_service.get_all_users(page=page, page_size=page_size)
    return FullUserListResponse(
        status_code=0,
        detail='string',
        result=UserList(
            users=users
        ),
        pagination=Pagination(
            current_page=page,
            total_page=ceil(total_users / page_size),
            total_results=total_users
        )
    )


@user_router.get("/{user_id}", response_model=FullUserResponse)
async def get_user(user_id: int, user_service: UserService = Depends(get_user_service)) -> FullUserResponse:
    user = await user_service.get_user_by_id(user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return FullUserResponse(
        status_code=0,
        detail="string",
        result=UserResponseModel(
            user_id=user.user_id,
            user_email=user.user_email,
            user_firstname=user.user_firstname,
            user_lastname=user.user_lastname,
            user_avatar=user.user_avatar,
            user_status=user.user_status,
            user_city=user.user_city,
            user_phone=user.user_phone,
            user_password=user.user_password,
            user_links=user.user_links,
            is_superuser=user.is_superuser
        )
    )


@user_router.post("/", response_model=FullUserResponse)
async def create_new_user(user_data: UserCreate,
                          user_service: UserService = Depends(get_user_service)) -> FullUserResponse:
    user = await user_service.create_user(user_data=user_data)
    return FullUserResponse(
        status_code=0,
        detail="string",
        result=UserResponseModel(
            user_id=user.user_id,
            user_email=user.user_email,
            user_firstname=user.user_firstname,
            user_lastname=user.user_lastname,
            user_avatar=user.user_avatar,
            user_status=user.user_status,
            user_city=user.user_city,
            user_phone=user.user_phone,
            user_password=user.user_password,
            user_links=user.user_links,
            is_superuser=user.is_superuser
        )
    )


@user_router.put("/{user_id}", response_model=FullUserResponse)
async def update_existing_user(user_id: int, user_data: UserUpdate,
                               user_service: UserService = Depends(get_user_service)) -> FullUserResponse:
    user = await user_service.update_user(user_id=user_id, user_data=user_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return FullUserResponse(
        status_code=0,
        detail="string",
        result=UserResponseModel(
            user_id=user.user_id,
            user_email=user.user_email,
            user_firstname=user.user_firstname,
            user_lastname=user.user_lastname,
            user_avatar=user.user_avatar,
            user_status=user.user_status,
            user_city=user.user_city,
            user_phone=user.user_phone,
            user_password=user.user_password,
            user_links=user.user_links,
            is_superuser=user.is_superuser
        )
    )


@user_router.delete("/{user_id}", response_model=DeleteUserResponse)
async def delete_existing_user(user_id: int,
                               user_service: UserService = Depends(get_user_service)) -> DeleteUserResponse:
    user_id = await user_service.delete_user(user_id=user_id)
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")
    return DeleteUserResponse(
        status_code=200,
        detail="User delete successfully",
        result={
            "user_id": user_id
        }
    )
