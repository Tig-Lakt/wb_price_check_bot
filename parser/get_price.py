import os
import sys
import json
import time
import asyncio

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_PATH)

from rabbitmq import send_message
from database.database import get_book_data

from config import (
    DEST,
    CURRENCY,
)


async def get_price(vendor_code: str,) -> tuple[float, str]:
    """
    Получает цену по артикулу с использованием API Wildberries.

    Args:
        vendor_code (str): Артикул книги.

    Returns:
        tuple[float, str]: Кортеж, содержащий цену товара (str) и наименование товара (str).
                           Возвращает (None, None) в случае ошибки.
        После успешного получения или ошибки, отправляет данные (vendor_code и цену)
        в систему обмена сообщениями RabbitMQ через функцию `send_message`.
    """
    driver = await create_driver()
    price = None
    try:
        url = f'''https://card.wb.ru/cards/v1/detail?appType=1&curr={CURRENCY}&dest={DEST}&spp=27&nm={vendor_code}'''
        driver.get(url)
        time.sleep(5)
        data = driver.find_element(By.TAG_NAME, 'pre')
        json_data = json.loads(data.text)
        price = json_data['data']['products'][0]['salePriceU'] / 100
        
    except Exception as e:
        print(e)

    finally:
        driver.close()
        driver.quit()
        if price == None:
            price = 'Нет в наличии'
        data = {'book_id': '', 'price': ''}        
        data['book_id'] = f'{vendor_code}'
        data['price'] = price
        
        await send_message(data)


async def create_driver() -> webdriver.Chrome:
    """
    Создает и настраивает экземпляр веб-драйвера Chrome для Selenium.

    Returns:
        webdriver.Chrome: Настроенный веб-драйвер Chrome.
    """
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(options=chrome_options)

    return driver


async def get_books_id():
    """
    Получает все артикулы из базы данных.
    """
    books_id = await get_book_data()
    for book_id in books_id:
        await get_price(book_id['book_id'])

if __name__ == "__main__":
    asyncio.run(get_books_id())