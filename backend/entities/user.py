from dataclasses import dataclass

from typing_extensions import NewType

UserID = NewType("UserID", int)


@dataclass
class User:
    id: UserID
    name: str
