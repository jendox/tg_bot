from aiohttp_apispec import querystring_schema, response_schema, docs, request_schema

from backend.services.database import Question, Answer
from backend.services.web.app import View
from backend.services.web.mixins import AuthRequiredMixin
from backend.services.web.schemes import OkResponseSchema
from backend.services.web.store.quiz.schemes import (
    QuestionRequestIdSchema,
    QuestionListSchema,
    QuestionSchema,
    QuestionRequestDeleteSchema
)
from backend.services.web.utils import json_response


class QuestionListView(AuthRequiredMixin, View):
    @docs(
        tags=["quiz"],
        summary="Lists questions",
        description="Lists questions from the database"
    )
    @querystring_schema(QuestionRequestIdSchema)
    @response_schema(QuestionListSchema)
    async def get(self):
        query_params = self.request.query_string
        question_id = None
        if query_params != "":
            question_id = int(query_params.split("=")[-1])
        questions = await self.store.quizz.list_questions(question_id=question_id)

        return json_response(
            QuestionListSchema().dump(
                {
                    "questions": [QuestionSchema().dump(question) for question in questions]
                }
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

        return json_response()


class QuestionAddView(AuthRequiredMixin, View):
    @docs(
        tags=["quiz"],
        summary="Add a new question",
        description="Add a new question to the database"
    )
    @request_schema(QuestionSchema)
    @response_schema(QuestionSchema)
    async def post(self):
        question = Question(
            title=self.data["title"],
            answers=[Answer(**answer) for answer in self.data["answers"]],
        )
        question = await self.store.quizz.add_question(question)
        return json_response(QuestionSchema().dump(question))
