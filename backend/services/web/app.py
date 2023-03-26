from typing import Optional

from aiohttp.web import (
    Application as AiohttpApplication,
    Request as AiohttpRequest,
    View as AiohttpView,
)
from aiohttp_apispec import setup_aiohttp_apispec
from aiohttp_session import setup as session_setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from backend.config import AppConfig
from backend.entities.admin import Admin
from backend.services.database.database.base import Database
from backend.services.web.logger import setup_logging
from backend.services.web.middlewares import setup_middlewares
from backend.services.web.routes import setup_routes
from backend.services.web.store import setup_store, Store


# from app.store import Store, setup_store
# from app.web.logger import setup_logging


class Application(AiohttpApplication):
    config: Optional[AppConfig] = None
    store: Optional[Store] = None
    database: Optional[Database] = None


class Request(AiohttpRequest):
    admin: Optional[Admin] = None

    @property
    def app(self) -> Application:
        return super().app()


class View(AiohttpView):
    @property
    def request(self) -> Request:
        return super().request

    @property
    def database(self):
        return self.request.app.database

    @property
    def store(self) -> Store:
        return self.request.app.store

    @property
    def data(self) -> dict:
        return self.request.get("data", {})


app = Application()


def setup_app() -> Application:
    setup_logging(app)
    app.config = AppConfig()
    session_setup(app, EncryptedCookieStorage(app.config.session.key))
    setup_routes(app)
    setup_aiohttp_apispec(
        app, title="Telegram Bot", url="/docs/json", swagger_path="/docs"
    )
    setup_middlewares(app)
    setup_store(app)
    return app
