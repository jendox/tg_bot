from aiohttp_apispec import querystring_schema, response_schema, docs, request_schema

from backend.services.web.app import View
from backend.services.web.mixins import AuthRequiredMixin
from backend.services.web.schemes import OkResponseSchema
from backend.services.web.store.quiz.schemes import (
    QuestionsListSchema,
    QuestionResponseSchema,
    QuestionRequestIdSchema,
    QuestionRequestDeleteSchema,
)
from backend.services.web.utils import json_response


class QuestionListView(AuthRequiredMixin, View):
    @docs(
        tags=["quiz"],
        summary="Lists questions",
        description="Lists questions from the database"
    )
    @querystring_schema(QuestionRequestIdSchema)
    @response_schema(QuestionsListSchema)
    async def get(self):
        query_params = self.request.query_string
        question_id = None
        if query_params != "":
            question_id = int(query_params.split("=")[-1])
        questions = await self.store.quizz.list_questions(question_id=question_id)

        return json_response(
            QuestionsListSchema().dump(
                {"questions": [QuestionResponseSchema().dump(question) for question in questions]}
            )
        )


class QuestionDeleteView(AuthRequiredMixin, View):
    @docs(
        tags=["quiz"],
        summary="Delete a question",
        description="Delete a question from the database"
    )
    @request_schema(QuestionRequestDeleteSchema)
    @response_schema(OkResponseSchema)
    async def post(self):
        question_id = self.data["id"]
        await self.store.quizz.delete_question(question_id=question_id)

        return json_response(
        )

# class QuestionAddView(AuthRequiredMixin, View):
#     @docs(
#         tags=["quiz"],
#         summary="Add a new theme",
#         description="Add a new theme to the database"
#     )
#     @request_schema(ThemeSchema)
#     @response_schema(ThemeSchema)
#     async def post(self):
#         title = self.data["title"]
#         theme = await self.store.quizzes.create_theme(title=title)
#
#         return json_response(data=ThemeSchema().dump(theme))


# class QuestionAddView(AuthRequiredMixin, View):
#     @docs(
#         tags=["quiz"],
#         summary="Add a new question",
#         description="Add a new question to the database"
#     )
#     @request_schema(QuestionSchema)
#     @response_schema(QuestionSchema)
#     async def post(self):
#         title = self.data["title"]
#         theme_id = self.data["theme_id"]
#         answers = [Answer(answer["title"], answer["is_correct"]) for answer in self.data["answers"]]
#         await check_question(self.request.app, title, theme_id, answers)
#         question = await self.request.app.store.quizzes.create_question(title, theme_id, answers)
#
#         return json_response(data=QuestionSchema().dump(question))
#
#
# class QuestionListView(AuthRequiredMixin, View):
#     @docs(
#         tags=["quiz"],
#         summary="Lists questions by theme id",
#         description="Lists questions by theme id from the database"
#     )
#     @querystring_schema(ThemeIdSchema)
#     @response_schema(ListQuestionSchema)
#     async def get(self):
#         try:
#             theme_id = self.request["querystring"]["theme_id"]
#         except KeyError as e:
#             theme_id = None
#         questions = await self.request.app.store.quizzes.list_questions(theme_id=theme_id)
#         raw_questions = [QuestionSchema().dump(question) for question in questions]
#         return json_response(data={"questions": raw_questions})
