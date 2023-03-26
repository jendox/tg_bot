from dataclasses import dataclass

from typing_extensions import NewType

from backend.entities.answer import Answer

QuestionID = NewType("QuestionID", int)


@dataclass
class Question:
    id: QuestionID
    title: str
    answer: Answer
