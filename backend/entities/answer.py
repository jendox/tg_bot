from dataclasses import dataclass

from typing_extensions import NewType

AnswerID = NewType("AnswerID", int)


@dataclass
class Answer:
    id: AnswerID
    title: str
    score: int
