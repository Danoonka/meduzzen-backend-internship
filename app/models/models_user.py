from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field
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
    companies = relationship("Action", back_populates="user")


class CompanyDB(Base):
    __tablename__ = "companies"

    company_id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String)
    company_description = Column(String)
    owner_id = Column(Integer)
    company_visible = Column(Boolean, default=True)
    company_avatar = Column(String)
    users = relationship("Action", back_populates="company")


class Action(Base):
    __tablename__ = "actions"
    action_id = Column(Integer(), primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey('users.user_id'))
    user = relationship("User", back_populates="companies")
    company_id = Column(ForeignKey('companies.company_id'))
    company = relationship("CompanyDB", back_populates="users")
    action_type = Column(String)


class UserResponseModel(BaseModel):
    user_id: int
    user_email: str
    user_firstname: str
    user_lastname: str
    user_avatar: Optional[str] = None
    user_status: Optional[str] = None
    user_city: Optional[str] = None
    user_phone: Optional[int] = None
    user_links: List[str] = []
    is_superuser: bool = Field(default=False)


class UserLink(Base):
    __tablename__ = 'user_links'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    link = Column(String)


class UserBase(BaseModel):
    user_id: int
    user_email: str
    user_firstname: str
    user_lastname: str
    user_avatar: Optional[str] = None


class UserCreate(UserBase):
    user_email: str
    user_firstname: str
    user_lastname: str
    user_password: str


class UserUpdate(BaseModel):
    user_firstname: str
    user_lastname: str
    user_avatar: Optional[str] = None
    user_avatar: str
    user_status: str
    user_city: str
    user_phone: int


class Pagination(BaseModel):
    current_page: int
    total_page: int
    total_results: int


class UserList(BaseModel):
    users: List[UserBase]


class FullUserListResponse(BaseModel):
    status_code: int
    detail: str
    result: UserList
    pagination: Pagination


class UserSignUpRequest(BaseModel):
    user_email: str
    user_password: str
    user_firstname: str
    user_lastname: str


class UserId(BaseModel):
    user_id: int


class DeleteUserResponse(BaseModel):
    status_code: int
    detail: str
    result: UserId


class UserSignInResponse(BaseModel):
    access_token: str
    token_type: str


class FullUserResponse(BaseModel):
    status_code: int
    detail: str
    result: UserResponseModel


class GetAllUsers(BaseModel):
    user_list: list[UserBase]
    total_users: int


class CompanyCreateUpdate(BaseModel):
    company_name: str
    company_description: str


class Company(CompanyCreateUpdate):
    company_id: int
    owner_id: int
    company_visible: bool
    company_avatar: Optional[str] = None


class CompanyBase(BaseModel):
    company_id: int
    company_name: str
    company_avatar: Optional[str] = None


class GetAllCompanies(BaseModel):
    company_list: list[CompanyBase]
    total_companies: int


class CompanyResponse(BaseModel):
    company_id: int
    company_name: str
    company_description: str
    owner_id: int
    company_visible: bool
    company_avatar: Optional[str] = None


class FullCompanyResponse(BaseModel):
    status_code: int
    detail: str
    result: CompanyResponse


class CompanyList(BaseModel):
    companies: list[CompanyBase]


class FullCompanyListResponse(BaseModel):
    status_code: int
    detail: str
    result: CompanyList
    pagination: Pagination


class CompanyId(BaseModel):
    company_id: int


class DeleteCompanyResponse(BaseModel):
    status_code: int
    detail: str
    result: CompanyId
