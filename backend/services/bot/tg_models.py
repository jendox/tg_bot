from dataclasses import dataclass, field
from typing import Optional, List, Any


@dataclass
class User:
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str]
    username: str


@dataclass
class Chat:
    id: int
    type: str
    title: Optional[str]
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    pinned_message: Optional["Message"]


@dataclass
class MessageEntity:
    type: str
    offset: int
    length: int


@dataclass
class Message:
    message_id: int
    from_: Optional[User] = field(metadata={"name": "from"})
    date: int
    chat: Chat
    text: Optional[str] = None
    new_chat_member: Optional[User] = None
    entities: Optional[List[MessageEntity]] = None


@dataclass
class CallbackQuery:
    id: int
    data: str
    from_: Optional[User] = field(metadata={"name": "from"})
    message: Optional[Message]
    date: Optional[int]
    chat: Optional[Chat]


@dataclass
class Update:
    update_id: int
    message: Optional[Message] = None
    callback_query: Optional[CallbackQuery] = None
    state: Optional[Any] = None

    def set_state(self, state: Any):
        self.state = state


@dataclass
class ChatMember:
    status: str
    user: User
