from marshmallow import Schema, fields


class QuestionRequestIdSchema(Schema):
    id = fields.Int()


class QuestionRequestDeleteSchema(Schema):
    id = fields.Int(required=True)


class AnswerResponseSchema(Schema):
    id = fields.Int(required=True)
    title = fields.Str(required=True)
    score = fields.Int(required=True)


class QuestionResponseSchema(Schema):
    id = fields.Int(required=True)
    title = fields.Str(required=True)
    answers = fields.Nested(AnswerResponseSchema, many=True, required=True)


class QuestionsListSchema(Schema):
    questions = fields.Nested(QuestionResponseSchema, many=True, required=True)
