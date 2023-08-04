from pydantic import BaseModel


class ActionBase(BaseModel):
    action_id: int
    user_id: int
    company_id: int
    action_type: str


class FullActionResponse(BaseModel):
    status_code: int
    detail: str
    result: ActionBase

class DeleteActionResponse(BaseModel):
    status_code: int
    detail: str
    result: int


