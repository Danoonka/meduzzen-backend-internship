from pydantic import BaseModel


class QuestionBase(BaseModel):
    question_text: str
    question_answers: list[str]
    question_correct_answer: int


class QuizBase(BaseModel):
    quiz_id: int
    quiz_name: str
    quiz_frequency: int
    company_id: int
    created_by: int


class FullQuizBase(BaseModel):
    quiz_id: int
    quiz_name: str
    quiz_frequency: int
    company_id: int
    created_by: int
    question_list: list[QuestionBase]


class QuizToCreate(BaseModel):
    quiz_name: str
    quiz_frequency: int
    question_list: list[QuestionBase]


class QuizToUpdate(BaseModel):
    quiz_name: str
    quiz_title: str
    quiz_description: str
    quiz_frequency: int


class FullQuizResponse(BaseModel):
    status_code: int
    detail: str
    result: QuizBase


class DeleteQuizResponse(BaseModel):
    status_code: int
    detail: str
    result: int


class QuizListResponse(BaseModel):
    status_code: int
    detail: str
    result: list[QuizBase]


class RateBase(BaseModel):
    type: str
    rate: int
