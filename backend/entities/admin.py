from dataclasses import dataclass
from hashlib import sha256
from typing import Optional

from typing_extensions import NewType

AdminId = NewType("AdminId", int)


@dataclass
class Admin:
    id: AdminId
    email: str
    password: Optional[str] = None

    def is_password_valid(self, password: str):
        return self.password == sha256(password.encode()).hexdigest()

    @classmethod
    def from_session(cls, session: Optional[dict]) -> Optional["Admin"]:
        return cls(id=session["admin"]["id"], email=session["admin"]["email"])
