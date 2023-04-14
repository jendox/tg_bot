import typing
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.entities import Answer as AnswerEntity, Game
from backend.services.database.database.sqlalchemy_base import db
if typing.TYPE_CHECKING:
    from backend.services.database import Question, games_answers_table


class Answer(db, AnswerEntity):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    score: Mapped[int] = mapped_column(nullable=False)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id", ondelete="CASCADE"))
    question: Mapped["Question"] = relationship("Question", back_populates="answers")

    games: Mapped[List["Game"]] = relationship(
        argument="Game", secondary="games_answers_table", back_populates="answers"
    )
