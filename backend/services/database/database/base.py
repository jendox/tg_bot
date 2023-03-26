from typing import Optional, TYPE_CHECKING
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from app.store.database import db

if TYPE_CHECKING:
    from app.web.app import Application


class Database:
    def __init__(self, app: "Application"):
        self.app = app
        self._engine: Optional[AsyncEngine] = None
        self._db: Optional[declarative_base] = None
        self.session: Optional[AsyncSession] = None

    def _get_database_url(self) -> str:
        return f'postgresql+asyncpg://' \
               f'{self.app.config.database.user}:' \
               f'{self.app.config.database.password}@' \
               f'{self.app.config.database.host}:' \
               f'{self.app.config.database.port}/' \
               f'{self.app.config.database.database}'

    async def connect(self, *_: list, **__: dict) -> None:
        self._db = db
        self._engine = create_async_engine(url=self._get_database_url(), echo=True)
        self.session = async_sessionmaker(bind=self._engine, class_=AsyncSession, expire_on_commit=False)

    async def disconnect(self, *_: list, **__: dict) -> None:
        if self._engine:
            await self._engine.dispose()
