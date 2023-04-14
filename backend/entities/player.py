import typing
from dataclasses import dataclass

from typing_extensions import NewType

if typing.TYPE_CHECKING:
    from backend.entities import Answer, User

PlayerId = NewType("PlayerId", int)


@dataclass
class Player:
    id: PlayerId
    user: "User"
    points: int = 0
    answer: "Answer" = None
    active: bool = True
