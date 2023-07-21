from typing import Optional

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, EmailStr, Field
from typing_extensions import List

Base = declarative_base()
metadata = MetaData()


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer(), primary_key=True, nullable=False)
    user_email = Column(String, nullable=False)
    user_firstname = Column(String, nullable=False)
    user_lastname = Column(String, nullable=False)
    user_avatar = Column(String, nullable=True)
    user_status = Column(String, nullable=True)
    user_city = Column(String, nullable=True)
    user_phone = Column(Integer, nullable=True)
    user_password = Column(String, nullable=False)
    user_links = relationship("UserLink", backref="user")
    is_superuser = Column(Boolean, default=False)


class UserResponseModel(BaseModel):
    user_id: int
    user_email: str
    user_firstname: str
    user_lastname: str
    user_avatar: Optional[str] = None
    user_status: Optional[str] = None
    user_city: Optional[str] = None
    user_phone: Optional[int] = None
    user_password: str
    user_links: List[str] = []
    is_superuser: bool = Field(default=False)

    class Config:
        orm_mode = True


class UserLink(Base):
    __tablename__ = 'user_links'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    link = Column(String)


class UserBase(BaseModel):
    user_email: str
    user_firstname: str
    user_lastname: str


class UserCreate(UserBase):
    user_password: str


class UserUpdate(UserBase):
    user_avatar: str
    user_status: str
    user_city: str
    user_phone: int


class UserList(BaseModel):
    users: List[UserResponseModel]


class UserSignInRequest(BaseModel):
    user_email: str
    user_password: str


class UserSignUpRequest(BaseModel):
    user_email: str
    user_password: str
    user_firstname: str
    user_lastname: str


class DeleteUserResponse(BaseModel):
    status_code: int
    detail: str
    result: dict
