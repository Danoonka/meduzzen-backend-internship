from datetime import timedelta, datetime
import jwt
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from typing_extensions import Awaitable

from config import SECRET_KEY, ALGORITHM, DOMAIN, ALGORITHMS, API_AUDIENCE, ISSUER


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


class VerifyToken:
    def __init__(self, token):
        self.token = token
        jwks_url = f'https://{DOMAIN}/.well-known/jwks.json'
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    def verify(self):
        try:
            self.signing_key = self.jwks_client.get_signing_key_from_jwt(
                self.token
            ).key
        except jwt.exceptions.PyJWKClientError as error:
            return {"status": "error", "msg": error.__str__()}
        except jwt.exceptions.DecodeError as error:
            return {"status": "error", "msg": error.__str__()}

        try:
            payload = jwt.decode(
                self.token,
                self.signing_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=ISSUER,
            )
        except Exception as e:
            return {"status": "error", "message": str(e)}

        return payload


def is_token_from_app(token: HTTPAuthorizationCredentials):
    try:
        encoded_token = token.credentials.encode('utf-8')
        decoded_token = jwt.decode(encoded_token, SECRET_KEY, algorithms=["HS256"])
        app_token_claim = decoded_token.get('app_token', False)
        return app_token_claim
    except jwt.exceptions.DecodeError:
        return False
