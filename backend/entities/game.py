import enum
import typing
from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from typing_extensions import NewType

if typing.TYPE_CHECKING:
    from backend.entities import Player, Question, Answer

GameId = NewType("GameId", int)
ChatId = NewType("ChatId", int)


class GameState(enum.Enum):
    creating = 1
    running = 2
    finished = 3


@dataclass
class Game:
    id: GameId
    chat_id: ChatId
    players: List["Player"] = field(default_factory=list)
    question: "Question" = None
    answers: List["Answer"] = field(default_factory=list)
    game_state: GameState = GameState.creating
    created_at: datetime = datetime.now()
    finished_at: datetime = None
