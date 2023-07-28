from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.routers.authintification import auth_router
from app.routers.user import user_router

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


app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
