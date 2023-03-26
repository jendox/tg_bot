import os
from dataclasses import dataclass, field


@dataclass(slots=True)
class BotConfig:
    token: str = field(init=False)
    timeout: int = field(init=False)

    def __post_init__(self):
        self._read_config()

    def _read_config(self):
        self.token = os.getenv("BOT_TOKEN")
        self.timeout = int(os.getenv("UPDATE_TIMEOUT"))


@dataclass(slots=True)
class RabbitConfig:
    username: str = field(init=False)
    password: str = field(init=False)
    host: str = field(init=False)
    port: str = field(init=False)
    queue: str = field(init=False)
    url: str = field(init=False)

    def __post_init__(self):
        self._read_config()

    def _read_config(self):
        self.username = os.getenv("RABBIT_USERNAME")
        self.password = os.getenv("RABBIT_PASSWORD")
        self.host = os.getenv("RABBIT_HOST")
        self.port = os.getenv("RABBIT_PORT")
        self.queue = os.getenv("RABBIT_QUEUE")
        self.url = f"amqp://{self.username}:{self.password}@" \
                   f"{self.host}:{self.port}/"


@dataclass(slots=True)
class DatabaseConfig:
    user: str = field(init=False)
    password: str = field(init=False)
    host: str = field(init=False)
    port: str = field(init=False)
    db: str = field(init=False)
    url: str = field(init=False)

    def __post_init__(self):
        self._read_config()

    def _read_config(self):
        self.user = os.getenv("POSTGRES_USER")
        self.password = os.getenv("POSTGRES_PASSWORD")
        self.host = os.getenv("POSTGRES_HOST")
        self.port = os.getenv("POSTGRES_PORT")
        self.db = os.getenv("POSTGRES_DB")
        self.url = f"postgres+asyncpg://{self.user}:{self.password}@" \
                   f"{self.host}:{self.port}/{self.db}"


@dataclass(slots=True)
class AdminConfig:
    email: str = field(init=False)
    password: str = field(init=False)

    def __post_init__(self):
        self._read_config()

    def _read_config(self):
        self.email = os.getenv("ADMIN_EMAIL")
        self.password = os.getenv("ADMIN_PASSWORD")


@dataclass(slots=True)
class AppConfig:
    bot: BotConfig = field(init=False, default_factory=BotConfig)
    rabbit: RabbitConfig = field(init=False, default_factory=RabbitConfig)
    db: DatabaseConfig = field(init=False, default_factory=DatabaseConfig)
    admin: AdminConfig = field(init=False, default_factory=AdminConfig)

