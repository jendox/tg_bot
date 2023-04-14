import json
from typing import Optional

import aiohttp

from backend.services.bot.commands import BotCommand
from backend.services.bot.game.handler import GameHandler
from backend.services.bot.tg_models import Update, Message, User, Chat
from backend.services.database.database.base import Database


class Bot:
    def __init__(
            self,
            token: str,
            session: aiohttp.ClientSession,
            database: Database
    ):
        self._token = token
        self._api_url = f"https://api.telegram.org/bot{self._token}"
        self._session = session
        self._database = database
        self._handler = GameHandler(self)
        self._command = BotCommand(
            ["/start", "/game", "/join@KtsCourseBot", "/stat", "/stop"]
        )

    @property
    def database(self):
        return self._database

    async def stop(self):
        await self._session.close()

    async def handle_update(self, update: Update):
        print(update)
        if command := self._command.parse_command(update):
            await self._handler.run_command(command=command, update=update)

    async def send_message(
            self,
            chat_id: int,
            text: str,
            reply_markup: Optional[dict] = None,
            parse_mode: str = "HTML"
    ) -> Message:
        url = f"{self._api_url}/sendMessage"
        params = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode,
        }
        if reply_markup:
            params["reply_markup"] = json.dumps(reply_markup)

        async with self._session.get(url=url, params=params) as resp:
            resp.raise_for_status()
            data = await resp.text()
            return Message(**json.loads(data)["result"])

    async def get_me(self):
        url = f"{self._api_url}/getMe"
        async with self._session.get(url) as resp:
            resp.raise_for_status()
            data = await resp.text()
            return User(**json.loads(data)["result"])

    async def get_chat(self, chat_id: int) -> Chat:
        url = f"{self._api_url}/getChat"
        params = {
            "chat_id": chat_id
        }
        async with self._session.get(url=url, params=params) as resp:
            resp.raise_for_status()
            data = await resp.text()
            return Chat(**json.loads(data)["result"])

    async def answer_callback_query(self, callback_query_id: int, text: str, show_alert: bool = True):
        url = f"{self._api_url}/answerCallbackQuery"
        params = {
            "callback_query_id": callback_query_id,
            "text": text,
            "show_alert": 1 if show_alert else 0
        }
        async with self._session.get(url=url, params=params) as resp:
            resp.raise_for_status()
            data = await resp.text()
            return json.loads(data)
