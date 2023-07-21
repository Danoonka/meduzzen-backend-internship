from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.db.db_postgres_handler import get_session
from app.models.models_authintification import LoginResponse, UserLogInRequest, TokenModel
from app.models.models_user import UserResponseModel, FullUserResponse
from app.services.authintification import AuthService
from app.utils.utils import create_access_token, get_user_from_token

auth_router = APIRouter()
token_auth_scheme = HTTPBearer()


async def get_auth_service(session: AsyncSession = Depends(get_session)) -> AuthService:
    return AuthService(session)


@auth_router.post('/login', response_model=LoginResponse)
async def authorize(data: UserLogInRequest,
                    auth_service: AuthService = Depends(get_auth_service)) -> LoginResponse:
    user = await auth_service.authenticate_user(username=data.user_email, password=data.user_password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_token_model = UserResponseModel(
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
    access_token = create_access_token(
        data={"user": user_token_model.dict()}, )
    return LoginResponse(
        status_code=0,
        detail='string',
        result=TokenModel(
            access_token=access_token,
            token_type="Bearer"
        )
    )


@auth_router.get("/me", response_model=FullUserResponse)
async def get_me(token: str = Header(None), auth_service: AuthService = Depends(get_auth_service)) -> FullUserResponse:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing access token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = get_user_from_token(token=token)
    if not user:
        user = await auth_service.create_user_from_auth0(token=token)
        return FullUserResponse(
            status_code=0,
            detail='string',
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
            ))
    return FullUserResponse(
        status_code=0,
        detail='string',
        result=user
    )
