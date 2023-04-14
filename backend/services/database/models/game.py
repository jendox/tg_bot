import typing
from datetime import datetime
from typing import List

from sqlalchemy import BIGINT, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.entities import Game as GameEntity, Answer
from backend.services.database import db

if typing.TYPE_CHECKING:
    from backend.services.database import Player, Question


games_answers_table = Table(
    "games_answers_table",
    db.metadata,
    Column("game_id", ForeignKey("games.id"), primary_key=True),
    Column("answer_id", ForeignKey("answers.id"), primary_key=True)
)


class Game(db, GameEntity):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(BIGINT(), nullable=False)
    game_state: Mapped[int] = mapped_column(default=1)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    finished_at: Mapped[datetime] = mapped_column(nullable=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))

    players: Mapped[List["Player"]] = relationship("Player", back_populates="game")
    question: Mapped["Question"] = relationship("Question", back_populates="games")
    answers: Mapped[List["Answer"]] = relationship(
        argument="Answer", secondary="games_answers_table", back_populates="games"
    )
