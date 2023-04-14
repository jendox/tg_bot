from dataclasses import dataclass, field
from typing import List

from typing_extensions import NewType

from backend.entities.answer import Answer

QuestionId = NewType("QuestionId", int)


@dataclass
class Question:
    id: QuestionId
    title: str
    answers: List[Answer] = field(default_factory=List)
