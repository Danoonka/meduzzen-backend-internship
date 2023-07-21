from pydantic import BaseModel


class TokenModel(BaseModel):
    access_token: str
    token_type: str


class LoginResponse(BaseModel):
    status_code: int
    detail: str
    result: TokenModel


class UserLogInRequest(BaseModel):
    user_email: str
    user_password: str



