import typing

from backend.services.web.store.quiz.views import (
    QuestionListView,
    QuestionDeleteView,
)

if typing.TYPE_CHECKING:
    from backend.services.web.app import Application


def setup_routes(app: "Application"):
    # app.router.add_view("/quiz.add_question", QuestionAddView)
    app.router.add_view("/quiz.delete_question", QuestionDeleteView)
    app.router.add_view("/quiz.list_questions", QuestionListView)
