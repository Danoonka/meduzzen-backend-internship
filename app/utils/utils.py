import string
from random import choice
from typing import Optional
import jwt
from passlib.context import CryptContext
from typing_extensions import Awaitable

from app.models.models_user import UserResponseModel, FullUserResponse, User
from config import SECRET_KEY, ALGORITHM, DOMAIN, ALGORITHMS, API_AUDIENCE, ISSUER


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def verify_password(plain_password: str, hashed_password: str) -> Awaitable[bool]:
    return pwd_context.verify(plain_password, hashed_password)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify(token: str) -> Optional[dict]:
    jwks_url = f'https://{DOMAIN}/.well-known/jwks.json'
    jwks_client = jwt.PyJWKClient(jwks_url)
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(
            token
        ).key
    except jwt.exceptions.PyJWKClientError:
        return False
    except jwt.exceptions.DecodeError:
        return False

    try:
        payload = jwt.decode(
            token,
            signing_key,
            algorithms=ALGORITHMS,
            audience=API_AUDIENCE,
            issuer=ISSUER,
        )
        return payload

    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
    except Exception:
        return False


def generate_temporary_password(length: int = 10) -> str:
    characters = string.ascii_letters + string.digits + string.punctuation
    temporary_password = ''.join(choice(characters) for _ in range(length))
    return temporary_password


def toUserResponse(user: User) -> UserResponseModel:
    user_response = UserResponseModel(
        user_id=user.user_id,
        user_email=user.user_email,
        user_firstname=user.user_firstname,
        user_lastname=user.user_lastname,
        user_avatar=user.user_avatar,
        user_status=user.user_status,
        user_city=user.user_city,
        user_phone=user.user_phone,
        user_links=user.user_links,
        is_superuser=user.is_superuser
    )

    return user_response


def toFullUserResponse(user: User) -> FullUserResponse:
    user = toUserResponse(user=user)

    full_user_response = FullUserResponse(
        status_code=0,
        detail="string",
        result=user
    )

    return full_user_response
