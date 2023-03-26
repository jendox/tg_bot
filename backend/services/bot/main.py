import asyncio

import aiohttp

from backend.config.config import AppConfig
from backend.services.bot.bot import Bot
from backend.services.rabbit.poller import RabbitPoller


async def run_service(
        token: str,
        rabbit_url: str,
        rabbit_queue: str
):
    client_session = aiohttp.ClientSession()

    bot = Bot(token, client_session)
    poller = RabbitPoller(rabbit_url, rabbit_queue, bot)

    try:
        await poller.start_polling()
    finally:
        await poller.stop()
        await bot.stop()


if __name__ == "__main__":
    config = AppConfig()
    try:
        asyncio.run(
            run_service(
                token=config.bot.token,
                rabbit_url=config.rabbit.url,
                rabbit_queue=config.rabbit.queue
            )
        )
    except KeyboardInterrupt:
        pass
