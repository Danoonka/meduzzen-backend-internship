from pydantic import BaseModel


class Invitation(BaseModel):
    user_id: int


class Request(BaseModel):
    company_id: int
