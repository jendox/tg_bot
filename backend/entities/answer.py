from dataclasses import dataclass

from typing_extensions import NewType

AnswerId = NewType("AnswerId", int)


@dataclass
class Answer:
    id: AnswerId
    title: str
    score: int
