from dataclasses import dataclass, field
from typing import List

from typing_extensions import NewType

from backend.entities.answer import Answer

QuestionID = NewType("QuestionID", int)


@dataclass
class Question:
    id: QuestionID
    title: str
    answers: List[Answer] = field(default_factory=List)
