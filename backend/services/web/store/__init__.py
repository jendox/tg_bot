import typing

from backend.services.database.database.base import Database

if typing.TYPE_CHECKING:
    from backend.services.web.app import Application


class Store:
    def __init__(self, app: "Application"):
        from backend.services.web.store.admin.accessor import AdminAccessor
        from backend.services.web.store.quiz.accessor import QuizAccessor

        self.quizz = QuizAccessor(app)
        self.admins = AdminAccessor(app)


def setup_store(app: "Application"):
    app.database = Database(app)
    app.on_startup.append(app.database.connect)
    app.on_cleanup.append(app.database.disconnect)
    app.store = Store(app)
