import string
from random import choice
from typing import Optional
import jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from typing_extensions import Awaitable
from config import SECRET_KEY, ALGORITHM, DOMAIN, ALGORITHMS, API_AUDIENCE, ISSUER


def create_access_token(data) -> str:
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_password_hash(password) -> str:
    return pwd_context.hash(password)


async def verify_password(plain_password, hashed_password) -> Awaitable[bool]:
    return pwd_context.verify(plain_password, hashed_password)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify(token) -> Optional[dict]:
    jwks_url = f'https://{DOMAIN}/.well-known/jwks.json'
    jwks_client = jwt.PyJWKClient(jwks_url)
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(
            token
        ).key
    except jwt.exceptions.PyJWKClientError as error:
        return {"status": "error", "msg": error.__str__()}
    except jwt.exceptions.DecodeError as error:
        return {"status": "error", "msg": error.__str__()}

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
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Token verification error: " + str(e))


def generate_temporary_password(length=10) -> str:
    characters = string.ascii_letters + string.digits + string.punctuation
    temporary_password = ''.join(choice(characters) for _ in range(length))
    return temporary_password


def get_user_from_token(token) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = payload["user"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        return False
    return user
