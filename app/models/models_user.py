from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, MetaData, ARRAY, Float, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field
from typing_extensions import List, Union, Dict
from _datetime import datetime

from app.models.models_company import CompanyBase

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
    quizzes = relationship("Quiz", back_populates="company")


class Action(Base):
    __tablename__ = "actions"
    action_id = Column(Integer(), primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey('users.user_id'))
    user = relationship("User", back_populates="companies")
    company_id = Column(ForeignKey('companies.company_id'))
    company = relationship("CompanyDB", back_populates="users")
    action_type = Column(String)


class Quiz(Base):
    __tablename__ = "quizzes"
    quiz_id = Column(Integer(), primary_key=True, index=True)
    quiz_name = Column(String)
    quiz_title = Column(String)
    quiz_description = Column(String)
    quiz_frequency = Column(Integer)
    created_by = Column(ForeignKey('users.user_id'))
    company_id = Column(ForeignKey('companies.company_id'))
    question_list = relationship("Question", back_populates="quiz")
    company = relationship("CompanyDB", back_populates="quizzes")


class Result(Base):
    __tablename__ = "results"
    result_id = Column(Integer(), primary_key=True, index=True)
    right_answers = Column(Integer())
    answers = Column(Integer())
    company_id = Column(ForeignKey('companies.company_id'))
    user_id = Column(ForeignKey('users.user_id'))
    quiz_id = Column(ForeignKey('quizzes.quiz_id'))
    answer_list = relationship("Answer")
    passed_at = Column(DateTime, default=datetime.utcnow)


class Answer(Base):
    __tablename__ = "answers"
    answer_id = Column(Integer(), primary_key=True, index=True)
    quiz_id = Column(ForeignKey('quizzes.quiz_id'))
    answers = Column(JSONB)
    result_id = Column(ForeignKey('results.result_id'))


class Question(Base):
    __tablename__ = "questions"
    quiz_id = Column(ForeignKey('quizzes.quiz_id'))
    question_id = Column(Integer(), primary_key=True, index=True)
    question_text = Column(String)
    question_answers = Column(ARRAY(String))
    question_correct_answer = Column(Integer)
    quiz = relationship("Quiz", back_populates="question_list")


class UserLink(Base):
    __tablename__ = 'user_links'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    link = Column(String)


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


class UserBase(BaseModel):
    user_id: int
    user_email: str
    user_firstname: str
    user_lastname: str
    user_avatar: Optional[str] = None
    action_id: Optional[int] = None


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


class ListResponse(BaseModel):
    status_code: int
    detail: str
    result: Optional[Union[List[UserBase], List[CompanyBase]]] = None


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


# class AnswerBase(BaseModel):
#     question_id: int
#     answer_id: int


class AnswerList(BaseModel):
    answers: Dict[str, str]


class ResultBase(BaseModel):
    result_id: int
    right_answers: int
    answers: int
    company_id: int
    user_id: int
    quiz_id: int
