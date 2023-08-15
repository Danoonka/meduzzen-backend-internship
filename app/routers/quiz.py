from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db_postgres_handler import get_session
from app.models.models_quiz import QuizToCreate, QuizToUpdate, QuestionBase, FullQuizResponse, DeleteQuizResponse, \
    QuizListResponse
from app.models.models_user import FullUserResponse
from app.routers.actions import get_action_service
from app.routers.authintification import get_current_user
from app.routers.company import get_company_service
from app.services.actions import ActionsService
from app.services.company import CompanyService
from app.services.quiz import QuizService
from app.utils.utils import toFullQuizResponse

quiz_router = APIRouter()


async def get_quiz_service(session: AsyncSession = Depends(get_session)) -> QuizService:
    return QuizService(session)


def authorize_quiz_access(quiz_id_param_name: str):
    async def _authorize(quiz_id: int, current_user: FullUserResponse = Depends(get_current_user),
                         actions_service: ActionsService = Depends(get_action_service),
                         company_service: CompanyService = Depends(get_company_service),
                         quiz_service: QuizService = Depends(get_quiz_service)):
        quiz = await quiz_service.get_quiz_by_id(quiz_id=quiz_id)
        company = await company_service.get_company_by_id(company_id=quiz.company_id)
        admins = await actions_service.get_all_admins(company_id=company.company_id)
        is_admin = any(admin.get('user_id') == current_user.result.user_id for admin in admins)
        if company.owner_id == current_user.result.user_id or is_admin:
            return quiz, company
        else:
            raise HTTPException(status_code=403, detail="Unauthorized")

    return _authorize


@quiz_router.post('/create-quiz/company/{company_id}/', response_model=FullQuizResponse)
async def create_quiz_endpoint(company_id: int,
                               quiz_data: QuizToCreate, current_user: FullUserResponse = Depends(get_current_user),
                               actions_service: ActionsService = Depends(get_action_service),
                               company_service: CompanyService = Depends(get_company_service),
                               quiz_service: QuizService = Depends(get_quiz_service)) -> FullQuizResponse:
    company = await company_service.get_company_by_id(company_id=company_id)
    admins = await actions_service.get_all_admins(company_id=company_id)
    is_admin = any(admin.get('user_id') == current_user.result.user_id for admin in admins)
    if company.owner_id == current_user.result.user_id or is_admin:
        if len(quiz_data.question_list) < 2:
            raise HTTPException(status_code=400, detail="A quiz must have at least 2 questions.")
        for question in quiz_data.question_list:
            if len(question.question_answers) < 2:
                raise HTTPException(status_code=400, detail="Each question must have at least 2 answers.")
        quiz = await quiz_service.create_quiz(quiz_data=quiz_data, company_id=company_id,
                                              user_id=current_user.result.user_id)
        return toFullQuizResponse(quiz=quiz, status_code=200, detail="Quiz created successfully")
    else:
        raise HTTPException(status_code=403, detail="Unauthorized")


@quiz_router.put('/update-quiz/{quiz_id}/', response_model=FullQuizResponse)
async def update_quiz_endpoint(quiz_data: QuizToUpdate,
                               authorized_data=Depends(authorize_quiz_access('quiz_id')),
                               quiz_service: QuizService = Depends(get_quiz_service)) -> FullQuizResponse:
    quiz_to_update, company = authorized_data
    updated_quiz = await quiz_service.update_quiz(quiz=quiz_to_update, quiz_data=quiz_data)
    return toFullQuizResponse(quiz=updated_quiz, status_code=200, detail="Quiz updated successfully")


@quiz_router.delete('/delete-quiz/{quiz_id}', response_model=DeleteQuizResponse)
async def delete_quiz_endpoint(quiz_id: int,
                               authorized_data=Depends(authorize_quiz_access('quiz_id')),
                               quiz_service: QuizService = Depends(get_quiz_service)
                               ) -> DeleteQuizResponse:
    quiz_to_delete, _ = authorized_data
    deleted_quiz_id = await quiz_service.delete_quiz(quiz_id=quiz_id)
    return DeleteQuizResponse(
        status_code=200,
        detail="Quiz deleted successfully",
        result=deleted_quiz_id
    )


@quiz_router.get('/all-company-quiz/company/{company_id}', response_model=QuizListResponse)
async def get_all_company_quiz_endpoint(company_id: int,
                                        quiz_service: QuizService = Depends(get_quiz_service)) -> QuizListResponse:
    all_quizzes = await quiz_service.get_all_company_quiz(company_id=company_id)
    return QuizListResponse(
        status_code=200,
        detail="Get quiz list successfully",
        result=all_quizzes
    )


@quiz_router.post('/add-new-question/{quiz_id}', response_model=FullQuizResponse)
async def add_question_endpoint(quiz_id: int, question_data: QuestionBase,
                                authorized_data=Depends(authorize_quiz_access('quiz_id')),
                                quiz_service: QuizService = Depends(get_quiz_service)
                                ) -> FullQuizResponse:
    quiz = authorized_data[0]
    await quiz_service.add_question(quiz_id=quiz_id, question_data=question_data)
    return toFullQuizResponse(quiz=quiz, status_code=200, detail="Quiz updated successfully")


@quiz_router.put('/update-question/quiz/{quiz_id}/question/{question_id}/', response_model=FullQuizResponse)
async def update_question_endpoint(question_id: int, question_data: QuestionBase,
                                   authorized_data=Depends(authorize_quiz_access('quiz_id')),
                                   quiz_service: QuizService = Depends(get_quiz_service)
                                   ) -> FullQuizResponse:
    quiz = authorized_data[0]
    if len(question_data.question_answers) < 2:
        raise HTTPException(status_code=400, detail="Question must have at least 2 answers")
    await quiz_service.update_question(question_id=question_id, question_data=question_data)
    return toFullQuizResponse(quiz=quiz, status_code=200, detail="Quiz updated successfully")


@quiz_router.delete('/delete-question/quiz/{quiz_id}/question/{question_id}', response_model=DeleteQuizResponse)
async def delete_question_endpoint(quiz_id: int, question_id: int,
                                   authorized_data=Depends(authorize_quiz_access('quiz_id')),
                                   quiz_service: QuizService = Depends(get_quiz_service)
                                   ) -> DeleteQuizResponse:
    quiz = authorized_data[0]
    await quiz_service.delete_question(question_id=question_id, quiz_id=quiz_id)
    return DeleteQuizResponse(
        status_code=200,
        detail="Question deleted successfully",
        result=question_id
    )


@quiz_router.get('/quiz/{quiz_id}', response_model=FullQuizResponse)
async def get_quiz_by_id_endpoint(authorized_data=Depends(authorize_quiz_access('quiz_id'))) -> FullQuizResponse:
    quiz = authorized_data[0]
    return toFullQuizResponse(
        status_code=200,
        detail="Get quiz successfully",
        quiz=quiz
    )
