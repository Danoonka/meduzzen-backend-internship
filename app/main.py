from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from app.routers.user import user_router, get_user_service
from app.services.user import UserService
from app.services.utils import VerifyToken, is_token_from_app

token_auth_scheme = HTTPBearer()

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


@app.get("/me", response_model=dict)
async def get_me(token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
                 user_service: UserService = Depends(get_user_service)) -> dict:
    if not is_token_from_app(token):
        current_user = user_service.get_user_from_token(token.credentials)
        print(current_user)
    else:
        cur_usr = VerifyToken(token).verify()

        if cur_usr.get("status"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=cur_usr)

        current_user = cur_usr

    return current_user


app.include_router(user_router, prefix="/users", tags=["users"])
