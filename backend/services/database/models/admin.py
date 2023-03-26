from sqlalchemy.orm import Mapped, mapped_column

from backend.entities.admin import Admin as AdminEntity
from backend.services.database.database.sqlalchemy_base import db


class Admin(db, AdminEntity):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
