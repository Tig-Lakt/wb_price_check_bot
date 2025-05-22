from aiogram import types
from aiogram import Router, F

from database.database import (
    get_book_price, 
)

from resources import (
    creating_book_kb,
    images,
)


router = Router()
    
    
@router.callback_query(F.data.startswith('book_id_'))
async def f_book_id(callback: types.CallbackQuery): 
    kb = await creating_book_kb()
    await callback.message.delete()
    book_id = callback.data[8:]    
    book_data = await get_book_price(int(book_id))
    
    msg_text = f"""
    Стоимость книги <b>{book_data[0]['book_name']}</b> составляет <b>{book_data[0]['price']}₽</b>
    """
    img = images[book_id]

    await callback.message.answer_photo(
        photo=img,
        caption=msg_text,
        reply_markup=kb.as_markup(resize_keyboard=True)
    )