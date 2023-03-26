import typing
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from backend.services.database import db
if typing.TYPE_CHECKING:
    from backend.services.web.app import Application


class Database:
    def __init__(self, app: "Application"):
        self._app = app
        self._engine: Optional[AsyncEngine] = None
        self._db: Optional[declarative_base] = None
        self.session: Optional[AsyncSession] = None

    async def connect(self, *_: list, **__: dict) -> None:
        self._db = db
        self._engine = create_async_engine(url=self._app.config.db.url, echo=True)
        self.session = async_sessionmaker(bind=self._engine, class_=AsyncSession, expire_on_commit=False)

    async def disconnect(self, *_: list, **__: dict) -> None:
        if self._engine:
            await self._engine.dispose()
