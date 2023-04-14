from dataclasses import dataclass
from typing import Optional

from typing_extensions import NewType


UserId = NewType("UserId", int)


@dataclass
class User:
    id: UserId
    is_bot: bool
    first_name: str
    username: str
    last_name: Optional[str] = None
