import os
import sys
import aio_pika
import json
from typing import Dict

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_PATH)

from config import (
    DB_CONN,
    RABBIT_LOGIN,
    RABBIT_PASSWORD,
    )


async def send_message(message_data: Dict):
    """
    Асинхронная функция для отправки сообщения в очередь RabbitMQ.
    """
    
    connection = await aio_pika.connect_robust(
        f"amqp://{RABBIT_LOGIN}:{RABBIT_PASSWORD}@{DB_CONN[0]}/"
    )
    try:
        channel = await connection.channel()

        await channel.declare_queue("my_queue")

        message_text = json.dumps(message_data)
        message = aio_pika.Message(message_text.encode())

        await channel.default_exchange.publish(
            message, routing_key="my_queue"
        )
        print(f"Отправлено сообщение: {message_data}")

    finally:
        await connection.close()