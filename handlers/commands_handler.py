from aiogram import types
from aiogram.filters.command import Command
from aiogram import Router

from resources import (
    creating_book_kb,
    welcome_text,
)

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    """
    Обработчик команды `/start`.

    Приветствует пользователя и предлагает выбрать название книги, чтобы отобразить ее стоимость.

    Args:
        message (types.Message): Объект сообщения от пользователя.
    """
    kb = await creating_book_kb()
    await message.answer(text=welcome_text,
                             reply_markup=kb.as_markup(resize_keyboard=True))