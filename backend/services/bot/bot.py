import json
from typing import Optional

import aiohttp

from backend.services.bot.tg_models import Update, Message, User, Chat


class Bot:
    def __init__(
            self,
            token: str,
            session: aiohttp.ClientSession,
    ):
        self._token = token
        self._api_url = f"https://api.telegram.org/bot{self._token}"
        self._session = session

    async def stop(self):
        await self._session.close()

    async def handle_update(self, update: Update):
        print(update)
        # raise NotImplementedError

    async def send_message(self, chat_id: int, text: str, reply_markup: Optional[dict] = None) -> Message:
        url = f"{self._api_url}/sendMessage"
        params = {
            "chat_id": chat_id,
            "text": text
        }
        if reply_markup:
            params["reply_markup"] = reply_markup

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

    async def get_chat(self, chat_id: int):
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
