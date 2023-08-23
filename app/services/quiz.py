import json
from typing import Optional

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.redistool.tools import add_quiz
from app.models.models_quiz import QuizToCreate, QuizToUpdate, QuestionBase, QuizBase, FullQuizBase, RedisResults
from app.models.models_user import Quiz, Question, AnswerList, Result, ResultBase, QuestionsForRedis


class QuizService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_quiz(self, quiz_data: QuizToCreate, company_id: int, user_id: int) -> QuizBase:
        quiz = Quiz(
            quiz_name=quiz_data.quiz_name,
            quiz_frequency=quiz_data.quiz_frequency,
            company_id=company_id,
            created_by=user_id
        )

        self.session.add(quiz)
        await self.session.flush()

        for question_data in quiz_data.question_list:
            await self._create_question(quiz_id=quiz.quiz_id, question_data=question_data)

        await self.session.commit()
        return quiz

    async def update_quiz(self, quiz: Quiz, quiz_data: QuizToUpdate) -> QuizBase:
        for field, value in quiz_data.dict(exclude_unset=True).items():
            setattr(quiz, field, value)

        await self.session.flush()
        await self.session.commit()
        return quiz

    async def delete_quiz(self, quiz_id: int) -> int:
        quiz = await self.get_quiz_by_id(quiz_id=quiz_id)

        if quiz:
            await self._delete_questions_by_quiz_id(quiz_id=quiz_id)
            await self.session.delete(quiz)
            await self.session.commit()
            return quiz.quiz_id
        else:
            raise Exception("Quiz does not exist")

    async def add_question(self, quiz_id, question_data: QuestionBase) -> QuestionBase:
        question = await self._create_question(quiz_id=quiz_id, question_data=question_data)
        await self.session.commit()
        return question

    async def update_question(self, question_id: int, question_data: QuestionBase) -> QuestionBase:
        question = await self.get_question_by_id(question_id=question_id)
        for field, value in question_data.dict(exclude_unset=True).items():
            setattr(question, field, value)

        await self.session.flush()
        await self.session.commit()
        return question

    async def delete_question(self, question_id: int, quiz_id: int) -> int:
        question = await self.get_question_by_id(question_id=question_id)
        questions_count = await self._get_question_count_by_quiz_id(quiz_id=quiz_id)

        if questions_count <= 2:
            raise Exception("Quiz must have at least 2 questions")

        if question:
            await self.session.delete(question)
            await self.session.flush()
            await self.session.commit()
            return question.quiz_id
        else:
            raise Exception("Question does not exist")

    async def get_quiz_by_id(self, quiz_id: int) -> FullQuizBase:
        quiz = await self.session.scalar(select(Quiz).where(Quiz.quiz_id == quiz_id).options(
            selectinload(Quiz.question_list)))
        return quiz

    async def get_question_by_id(self, question_id: int) -> QuestionBase:
        return await self.session.scalar(select(Question).where(Question.question_id == question_id))

    async def get_all_company_quiz(self, company_id: int) -> list[QuizBase]:
        quizzes = await self.session.execute(select(Quiz).where(Quiz.company_id == company_id))
        return [QuizBase(**quiz.__dict__) for quiz in quizzes.scalars().all()]

    async def _create_question(self, quiz_id, question_data: QuestionBase) -> QuestionBase:
        question = Question(
            quiz_id=quiz_id,
            question_text=question_data.question_text,
            question_answers=question_data.question_answers,
            question_correct_answer=question_data.question_correct_answer
        )

        if len(question.question_answers) < 2:
            raise Exception("Add more answers")

        self.session.add(question)
        return question

    async def _delete_questions_by_quiz_id(self, quiz_id: int) -> int:
        questions = await self.session.execute(select(Question).where(Question.quiz_id == quiz_id))
        for question in questions.scalars().all():
            await self.session.delete(question)
            return quiz_id

    async def _get_question_count_by_quiz_id(self, quiz_id: int) -> int:
        return await self.session.execute(select(Question).where(Question.quiz_id == quiz_id)).scalar()

    async def take_quiz(self, quiz_id: int, answers: AnswerList, company_id: int, user_id: int) -> Optional[ResultBase]:
        counter = 0
        quiz = await self.get_quiz_by_id(quiz_id=quiz_id)

        questions = []
        for question in quiz.question_list:
            item = QuestionsForRedis(
                question_id=str(question.question_id),
                question_text=question.question_text,
                answer=question.question_answers[int(answers.answers[str(question.question_id)])],
                isCorrect=question.question_correct_answer == int(answers.answers[str(question.question_id)])
            )
            question_dict = item.dict()
            question_json = json.dumps(question_dict)
            questions.append(question_json)
            if answers.answers[str(question.question_id)] == str(question.question_correct_answer):
                counter += 1

        new_result = Result(
            right_answers=counter,
            answers=len(quiz.question_list),
            company_id=company_id,
            user_id=user_id,
            quiz_id=quiz_id
        )

        self.session.add(new_result)
        await self.session.flush()
        await self.session.commit()
        await add_quiz(user_id=str(user_id),
                       company_id=str(company_id),
                       quiz_id=str(quiz_id),
                       questions=questions)
        return new_result

    async def get_global_rate_for_user(self, user_id) -> int:
        all_user_results = await self.session.execute(select(Result).where(Result.user_id == user_id))
        results = [ResultBase(**result.__dict__) for result in all_user_results.scalars().all()]

        right_answers = 0
        answers = 0
        for result in results:
            right_answers += result.right_answers
            answers += result.answers
        return round(right_answers / answers, 2)

    async def get_quiz_rate_for_user(self, user_id, quiz_id: int) -> int:
        all_user_results = await self.session.execute(
            select(Result).where(and_(Result.user_id == user_id, Result.quiz_id == quiz_id)))
        results = [ResultBase(**result.__dict__) for result in all_user_results.scalars().all()]

        right_answers = 0
        answers = 0
        for result in results:
            right_answers += result.right_answers
            answers += result.answers
        return round(right_answers / answers, 2)

    async def get_company_rate_for_user(self, user_id, company_id: int) -> int:
        all_user_results = await self.session.execute(
            select(Result).where(and_(Result.user_id == user_id, Result.company_id == company_id)))
        results = [ResultBase(**result.__dict__) for result in all_user_results.scalars().all()]

        right_answers = 0
        answers = 0
        for result in results:
            right_answers += result.right_answers
            answers += result.answers
        return round(right_answers / answers, 2)
