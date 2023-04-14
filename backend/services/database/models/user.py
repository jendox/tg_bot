from typing import List

from sqlalchemy import BIGINT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.entities.user import User as UserEntity
from backend.services.database import db
from backend.services.database.models.player import Player


class User(db, UserEntity):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BIGINT(), primary_key=True, autoincrement=False)
    is_bot: Mapped[bool] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(nullable=True)

    players: Mapped[List[Player]] = relationship("Player", back_populates="user")
