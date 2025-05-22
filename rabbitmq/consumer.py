import os
import sys
import asyncio
import aio_pika
import json

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_PATH)

from config import (
    DB_CONN,
    RABBIT_LOGIN,
    RABBIT_PASSWORD,
    )
from database.database import upd_book_data


async def process_message(message: aio_pika.abc.AbstractIncomingMessage):
    """
    Асинхронная функция для обработки входящих сообщений из очереди RabbitMQ.
    При успешно обработке отправляет данные для обновления записи в базу данных
    """
    async with message.process():
        body = message.body.decode()
        try:
            message_data = json.loads(body)
            await upd_book_data(str(message_data['price']), int(message_data['book_id']))
            print(f"Получено сообщение: {message_data}")
        except json.JSONDecodeError:
            print(f"Ошибка декодирования JSON: {body}")
            

async def main():
    """
    Основная асинхронная функция, устанавливающая соединение с RabbitMQ,
    подписывающаяся на очередь и ожидающая сообщений
    """
    connection = await aio_pika.connect_robust(
        f"amqp://{RABBIT_LOGIN}:{RABBIT_PASSWORD}@{DB_CONN[0]}/"
    )

    try:
        channel = await connection.channel()

        queue = await channel.declare_queue("my_queue")

        await queue.consume(process_message)

        print("Жду сообщений...")
        await asyncio.Future()

    finally:
        await connection.close()


if __name__ == "__main__":
    """Главная асинхронная функция для запуска получателя RabbitMQ.

        Эта функция содержит основную логику получателя сообщений, которая выполняется асинхронно.
        """
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Завершение работы...")