import asyncio
import json
import logging
import typing

import aio_pika
from aio_pika.abc import AbstractRobustConnection

from backend.services.bot.bot import Bot
from backend.services.bot.tg_models import Update

logger = logging.getLogger()


class RabbitPoller:
    def __init__(self, rabbit_url: str, rabbit_queue: str, bot: Bot):
        self._rabbit_url = rabbit_url
        self._rabbit_queue = rabbit_queue
        self._connection: typing.Optional[AbstractRobustConnection] = None
        self._bot = bot

    async def start_polling(self):
        logger.info("Starting RabbitPoller")
        self._connection = await aio_pika.connect_robust(self._rabbit_url)
        async with self._connection.channel() as channel:
            queue = await channel.declare_queue(self._rabbit_queue, durable=True)
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    try:
                        async with message.process():
                            task = asyncio.create_task(
                                self._bot.handle_update(Update(**json.loads(message.body)))
                            )
                            task.add_done_callback(self.handle_task)
                    except asyncio.TimeoutError:
                        await message.nack(requeue=True)
                    except Exception as e:
                        logger.exception(f"Error: {e}")
                        await message.reject(requeue=False)

    def handle_task(self, future: asyncio.Future):
        if exc := future.exception():
            logger.exception(f"Exception: {exc}")

    async def stop(self):
        if self._connection:
            await self._connection.close()
        logger.info("RabbitPoller stopped")
