from sqlalchemy import select, delete
from sqlalchemy.orm import immediateload

from backend.entities.question import QuestionId
from backend.services.database import Question
from backend.services.web.store.base.base_accessor import BaseAccessor


class QuizAccessor(BaseAccessor):
    async def list_questions(self, question_id: QuestionId = None) -> list[Question]:
        async with self.app.database.session() as session:
            if question_id:
                stmt = select(Question).filter_by(id=question_id).options(immediateload(Question.answers))
            else:
                stmt = select(Question).options(immediateload(Question.answers))
            result = await session.execute(stmt)
            questions = result.scalars().all()
            return questions

    async def delete_question(self, question_id: QuestionId):
        async with self.app.database.session() as session:
            try:
                stmt = delete(Question).where(Question.id == question_id)
                await session.execute(stmt)
                await session.commit()
            except Exception as e:
                self.logger.error(f"An error occurred when deleting question with id={question_id}: {e}")

    async def add_question(self, question: Question) -> Question | None:
        async with self.app.database.session() as session:
            try:
                session.add(question)
                await session.commit()
            except Exception as e:
                self.logger.error(f"An error occurred when adding question: {e}")
                return None
            return question
