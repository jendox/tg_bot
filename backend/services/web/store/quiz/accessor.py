from sqlalchemy import select, delete
from sqlalchemy.orm import immediateload

from backend.entities.question import QuestionID
from backend.services.database import Question
from backend.services.web.store.base.base_accessor import BaseAccessor


class QuizAccessor(BaseAccessor):
    async def list_questions(self, question_id: QuestionID = None) -> list[Question]:
        questions = []
        async with self.app.database.session() as session:
            if question_id:
                stmt = select(Question).filter_by(id=question_id).options(immediateload(Question.answers))
            else:
                stmt = select(Question).options(immediateload(Question.answers))
            result = await session.execute(stmt)
            questions = result.scalars().all()
        return questions

    async def delete_question(self, question_id: QuestionID):
        async with self.app.database.session() as session:
            stmt = delete(Question).where(id=question_id)
            print(stmt)
            try:
                result = await session.execute(stmt)
            except Exception as e:
                print(e)

    # async def list_questions(self, theme_id: int | None = None) -> list[Question]:
    #     async with self.app.database.session() as session:
    #         if theme_id:
    #             stmt = select(QuestionModel).filter_by(theme_id=theme_id).options(immediateload(QuestionModel.answers))
    #         else:
    #             stmt = select(QuestionModel).options(immediateload(QuestionModel.answers))
    #         result = await session.execute(stmt)
    #         questions = []
    #         for question in result.scalars().all():
    #             questions.append(
    #                 Question(
    #                     id=question.id,
    #                     title=question.title,
    #                     theme_id=question.theme_id,
    #                     answers=[Answer(answer.title, answer.is_correct) for answer in question.answers])
    #             )
    #
    #         return questions


    # async def create_theme(self, title: str) -> Theme:
    #     async with self.app.database.session() as session:
    #         theme = ThemeModel(title=title)
    #         async with session.begin():
    #             session.add(theme)
    #     return Theme(id=theme.id, title=theme.title)
    #
    # async def get_theme_by_title(self, title: str) -> Theme | None:
    #     async with self.app.database.session() as session:
    #         stmt = select(ThemeModel).filter_by(title=title)
    #         result = await session.execute(stmt)
    #         if result.raw.rowcount == 1:
    #             theme = result.scalars().one()
    #             return Theme(theme.id, theme.title)
    #         return None
    #
    # async def get_theme_by_id(self, id_: int) -> Theme | None:
    #     async with self.app.database.session() as session:
    #         stmt = select(ThemeModel).filter_by(id=id_)
    #         result = await session.execute(stmt)
    #         if result.raw.rowcount == 1:
    #             theme = result.scalars().one()
    #             return Theme(theme.id, theme.title)
    #         return None
    #
    # async def list_themes(self) -> list[Theme]:
    #     async with self.app.database.session() as session:
    #         stmt = select(ThemeModel)
    #         result = await session.execute(stmt)
    #         themes = []
    #         for row in result.scalars().all():
    #             themes.append(Theme(row.id, row.title))
    #         return themes
    #
    # async def create_answers(
    #     self, question_id: int, answers: list[Answer]
    # ) -> list[Answer]:
    #     answers_models = [
    #         AnswerModel(title=answer.title, question_id=question_id, is_correct=answer.is_correct) for answer in answers
    #     ]
    #     async with self.app.database.session() as session:
    #         async with session.begin():
    #             session.add_all(answers_models)
    #     return answers
    #
    # async def create_question(
    #     self, title: str, theme_id: int, answers: list[Answer]
    # ) -> Question:
    #     question = QuestionModel(title=title, theme_id=theme_id)
    #     async with self.app.database.session() as session:
    #         async with session.begin():
    #             session.add(question)
    #     await self.create_answers(question_id=question.id, answers=answers)
    #     return Question(question.id, title, theme_id, answers)
    #
    # async def get_question_by_title(self, title: str) -> Question | None:
    #     async with self.app.database.session() as session:
    #         stmt = select(QuestionModel).filter_by(title=title).options(immediateload(QuestionModel.answers))
    #         result = await session.execute(stmt)
    #         if result.raw.rowcount == 1:
    #             question = result.scalars().one()
    #             return Question(
    #                 id=question.id,
    #                 title=question.title,
    #                 theme_id=question.theme_id,
    #                 answers=[Answer(answer.title, answer.is_correct) for answer in question.answers])
    #         return None
    #
