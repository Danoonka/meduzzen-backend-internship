from math import ceil
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db_postgres_handler import get_session
from app.models.models_user import UserUpdate, DeleteUserResponse, \
    FullUserResponse, UserList, Pagination, FullUserListResponse, UserSignUpRequest, UserId
from app.routers.authintification import get_current_user
from app.services.user import UserService
from app.utils.utils import toFullUserResponse

user_router = APIRouter()


async def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(session)


@user_router.get("/", response_model=FullUserListResponse)
async def get_users(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1),
                    user_service: UserService = Depends(get_user_service)) -> FullUserListResponse:
    users_with_count = await user_service.get_all_users(page=page, page_size=page_size)
    return FullUserListResponse(
        status_code=0,
        detail='string',
        result=UserList(
            users=users_with_count.user_list
        ),
        pagination=Pagination(
            current_page=page,
            total_page=ceil(users_with_count.total_users / page_size),
            total_results=users_with_count.total_users
        )
    )


@user_router.get("/{user_id}", response_model=FullUserResponse)
async def get_user(user_id: int, user_service: UserService = Depends(get_user_service)) -> FullUserResponse:
    user = await user_service.get_user_by_id(user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return toFullUserResponse(user)


@user_router.post("/", response_model=FullUserResponse)
async def create_new_user(user_data: UserSignUpRequest,
                          user_service: UserService = Depends(get_user_service)) -> FullUserResponse:
    user = await user_service.create_user(user_data=user_data)
    return toFullUserResponse(user)


@user_router.put("/{user_id}", response_model=FullUserResponse)
async def update_existing_user(user_id: int, user_data: UserUpdate,
                               user_service: UserService = Depends(get_user_service),
                               current_user: FullUserResponse = Depends(get_current_user)) -> FullUserResponse:
    if current_user.result.user_id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    user = await user_service.update_user(user_id=user_id, user_data=user_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return toFullUserResponse(user)


@user_router.put("/{user_id}/password", response_model=FullUserResponse)
async def update_existing_user_password(user_id: int, user_password: str, new_password: str,
                                        user_service: UserService = Depends(get_user_service),
                                        current_user: FullUserResponse = Depends(get_current_user)) -> FullUserResponse:
    if current_user.result.user_id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    user = await user_service.update_user_password(user_id=user_id, user_password=user_password,
                                                   new_password=new_password)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return toFullUserResponse(user)


@user_router.delete("/{user_id}", response_model=DeleteUserResponse)
async def delete_existing_user(user_id: int,
                               user_service: UserService = Depends(get_user_service),
                               current_user: FullUserResponse = Depends(get_current_user)) -> DeleteUserResponse:
    if current_user.result.user_id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    user_id = await user_service.delete_user(user_id=user_id)
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")
    return DeleteUserResponse(
        status_code=200,
        detail="User delete successfully",
        result=UserId(
            user_id=user_id
        )
    )

