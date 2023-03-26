import asyncio
import aio_pika
import aiohttp

from backend.config.config import AppConfig

from backend.services.rabbit.publisher import (
    RabbitPublisher,
    Subscriber
)


async def run_service(
        token: str,
        timeout: int,
        rabbit_url: str,
        rabbit_queue: str
):
    connection = await aio_pika.connect_robust(rabbit_url)
    channel = await connection.channel()
    await channel.declare_queue(rabbit_queue, durable=True)
    client_session = aiohttp.ClientSession()

    publisher = RabbitPublisher(connection, channel, rabbit_queue)
    subscriber = Subscriber(token, timeout, publisher, client_session)

    try:
        await subscriber.start_polling()
    finally:
        await subscriber.stop()


if __name__ == "__main__":
    config = AppConfig()
    try:
        asyncio.run(
            run_service(
                token=config.bot.token,
                timeout=config.bot.timeout,
                rabbit_url=config.rabbit.url,
                rabbit_queue=config.rabbit.queue
            )
        )
    except KeyboardInterrupt:
        pass
