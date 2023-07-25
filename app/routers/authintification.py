from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.db.db_postgres_handler import get_session
from app.models.models_authintification import LoginResponse, UserLogInRequest, TokenModel
from app.models.models_user import UserResponseModel, FullUserResponse
from app.services.authintification import AuthService
from app.utils.utils import create_access_token, get_user_from_token, toFullUserResponse, toUserResponse

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
    user_token_model = toUserResponse(user)
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


async def get_current_user(token: str = Depends(token_auth_scheme),
                           auth_service: AuthService = Depends(get_auth_service)):
    token = token.credentials
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing access token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = get_user_from_token(token=token)
    if not user:
        user = await auth_service.create_user_from_auth0(token=token)
        return toFullUserResponse(user)
    return FullUserResponse(
        status_code=0,
        detail='string',
        result=user
    )


@auth_router.get("/me", response_model=FullUserResponse)
async def get_me(current_user: FullUserResponse = Depends(get_current_user)) -> FullUserResponse:
    return current_user
