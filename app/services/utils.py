from datetime import timedelta, datetime
import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from typing_extensions import Awaitable

from config import SECRET_KEY, ALGORITHM


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_password_hash(password) -> str:
    return pwd_context.hash(password)


async def verify_password(plain_password, hashed_password) -> Awaitable[bool]:
    return pwd_context.verify(plain_password, hashed_password)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
