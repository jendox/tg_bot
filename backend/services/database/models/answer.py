from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.entities.answer import Answer as AnswerEntity
from backend.services.database.database.sqlalchemy_base import db
from backend.services.database import Question


class Answer(db, AnswerEntity):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    score: Mapped[int] = mapped_column(nullable=False)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id", ondelete="CASCADE"))
    question: Mapped[Question] = relationship("Question", back_populates="answers")
