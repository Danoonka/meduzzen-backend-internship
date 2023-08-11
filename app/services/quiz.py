from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models_quiz import QuizToCreate, QuizToUpdate, QuestionBase, QuizBase
from app.models.models_user import Quiz, Question


class QuizService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_quiz(self, quizData: QuizToCreate, company_id: int, user_id: int) -> QuizBase:
        quiz = Quiz(
            quiz_name=quizData.quiz_name,
            quiz_frequency=quizData.quiz_frequency,
            company_id=company_id,
            created_by=user_id
        )

        self.session.add(quiz)
        await self.session.flush()
        for question_data in quizData.question_list:
            question = Question(
                quiz_id=quiz.quiz_id,
                question_text=question_data.question_text,
                question_answers=question_data.question_answers,
                question_correct_answer=question_data.question_correct_answer
            )
            self.session.add(question)
        await self.session.commit()

        return quiz

    async def get_quiz_by_id(self, quiz_id: int) -> QuizBase:
        quiz = await self.session.scalar(
            select(Quiz).where(Quiz.quiz_id == quiz_id)
        )
        return quiz

    async def get_question_by_id(self, question_id: int) -> QuestionBase:
        question = await self.session.scalar(
            select(Question).where(Question.question_id == question_id)
        )
        return question

    async def update_quiz(self, quiz, quiz_data: QuizToUpdate) -> QuizBase:
        quiz = await self.get_quiz_by_id(quiz_id=quiz.quiz_id)
        if quiz:
            for field, value in quiz_data.dict(exclude_unset=True).items():
                setattr(quiz, field, value)
            await self.session.flush()
            await self.session.commit()
            return quiz

    async def delete_quiz(self, quiz_id: int) -> int:
        quiz = await self.get_quiz_by_id(quiz_id=quiz_id)

        if quiz:
            questions = await self.session.execute(
                select(Question).where(Question.quiz_id == quiz_id))

            question_instances = [question[0] for question in questions]

            for question in question_instances:
                await self.session.delete(question)

            await self.session.delete(quiz)
            await self.session.commit()
            return quiz.quiz_id
        else:
            raise Exception("Quiz does not exist")

    async def get_all_company_quiz(self, company_id: int) -> list[QuizBase]:
        quizzes = await self.session.execute(
            select(Quiz).where(Quiz.company_id == company_id)
        )

        all_quizzes = [QuizBase(**quiz.__dict__) for quiz in quizzes.scalars().all()]

        return all_quizzes

    async def add_question(self, quiz_id, question_data: QuestionBase) -> QuestionBase:
        question = Question(
            quiz_id=quiz_id,
            question_text=question_data.question_text,
            question_answers=question_data.question_answers,
            question_correct_answer=question_data.question_correct_answer
        )

        if len(question.question_answers) < 2:
            raise Exception("Add more answers")

        self.session.add(question)
        await self.session.commit()
        return question

    async def update_question(self, question_id: int, question_data: QuestionBase) -> QuestionBase:
        question = await self.get_question_by_id(question_id=question_id)
        if question:
            for field, value in question_data.dict(exclude_unset=True).items():
                setattr(question, field, value)
            await self.session.flush()
            await self.session.commit()
            return question

    async def delete_question(self, question_id: int, quiz_id: int) -> int:
        question = await self.get_question_by_id(question_id=question_id)
        questions = await self.session.execute(
            select(Question).where(Question.quiz_id == quiz_id))

        question_instances = [question[0] for question in questions]
        if len(question_instances) == 2:
            raise ("Quiz can`t consist less then 2 question")
        if question:
            await self.session.delete(question)
            await self.session.flush()
            await self.session.commit()
            return question.quiz_id
        else:
            raise Exception("Question does not exist")
