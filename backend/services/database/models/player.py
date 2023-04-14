import typing

from sqlalchemy import ForeignKey, BIGINT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.entities.player import Player as PlayerEntity
from backend.services.database import db

if typing.TYPE_CHECKING:
    from backend.services.database import Game, User


class Player(db, PlayerEntity):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BIGINT(), ForeignKey("users.id"))
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))
    points: Mapped[int] = mapped_column(default=0)
    answer_id: Mapped[int] = mapped_column(ForeignKey("answers.id"), nullable=True)
    active: Mapped[bool] = mapped_column(default=True)

    user: Mapped["User"] = relationship("User", back_populates="players")
    game: Mapped["Game"] = relationship("Game", back_populates="players")
    # answer: Mapped["Answer"] = relationship("Answer", back_populates="players")
