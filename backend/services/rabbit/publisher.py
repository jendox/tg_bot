import asyncio
import json
import typing
import aio_pika
import aiohttp
import logging


logger = logging.getLogger()


class RabbitPublisher:
    def __init__(
            self,
            connection: aio_pika.abc.AbstractRobustConnection,
            channel: aio_pika.abc.AbstractRobustChannel,
            rabbit_queue: str
    ):
        self._connection = connection
        self._channel = channel
        self._rabbit_queue = rabbit_queue

    async def publish_update(self, update: dict):
        await self._channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(update).encode()),
            routing_key=self._rabbit_queue
        )

    async def close(self):
        await self._connection.close()


class Subscriber:
    def __init__(
            self,
            token: str,
            timeout: int,
            publisher: RabbitPublisher,
            session: aiohttp.ClientSession
    ):
        self._is_polling = None
        self._token = token
        self._publisher = publisher
        self._session = session
        self._timeout = timeout
        self._api_url = f"https://api.telegram.org/bot{self._token}"

    async def _get_updates(self, offset: typing.Optional[int] = None):
        url = f"{self._api_url}/getUpdates?timeout={self._timeout}"
        if offset:
            url += f"&offset={offset}"
        async with self._session.get(url) as resp:
            resp.raise_for_status()
            data = await resp.text()
            return json.loads(data)

    async def start_polling(self):
        offset = None
        self._is_polling = True
        while self._is_polling:
            try:
                updates = await self._get_updates(offset)
                if updates["ok"]:
                    updates = updates["result"]
                    for update in updates:
                        offset = update["update_id"] + 1
                        await self._process_update(update)
            except Exception as e:
                logger.exception(f"Error: {e}")
                await asyncio.sleep(2)

    async def _process_update(self, update: dict):
        try:
            await self._publisher.publish_update(update)
        except Exception as e:
            logger.exception(f"Error: {e}")

    async def stop(self):
        self._is_polling = False
        await self._session.close()
        await self._publisher.close()
