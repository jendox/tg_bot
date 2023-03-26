import typing

if typing.TYPE_CHECKING:
    from backend.services.web.app import Application


def setup_routes(app: "Application"):
    from backend.services.web.store.admin.routes import setup_routes as admin_setup_routes
    from backend.services.web.store.quiz.routes import setup_routes as quiz_setup_routes

    admin_setup_routes(app)
    quiz_setup_routes(app)
