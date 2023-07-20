from typing import Optional

from fastapi import FastAPI, Depends, Header, HTTPException
from starlette import status
from starlette.middleware.cors import CORSMiddleware

from app.models.models_user import UserResponseModel
from app.routers.user import user_router, get_user_service
from app.services.user import UserService

app = FastAPI()

origins = [
    "*"
    # "http://localhost",
    # "http://localhost:8000",
    # "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "status_code": 200,
        "detail": "ok",
        "result": "working"
    }


async def get_current_user(
        token: str = Header(None), user_service: UserService = Depends(get_user_service)) -> dict:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing access token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = user_service.get_user_from_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@app.get("/me", response_model=dict)
async def get_me(current_user: dict = Depends(get_current_user)) -> dict:
    return current_user


app.include_router(user_router, prefix="/users", tags=["users"])
