from dataclasses import dataclass
from typing import Optional

from typing_extensions import NewType

AdminID = NewType("AdminID", int)


@dataclass
class Admin:
    id: AdminID
    email: str
    password: Optional[str] = None
