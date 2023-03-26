from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.entities.answer import Answer
from backend.entities.question import Question as QuestionEntity
from backend.services.database.database.sqlalchemy_base import db


class Question(db, QuestionEntity):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    answer: Mapped[Answer] = relationship("Answer", back_populates="question")
