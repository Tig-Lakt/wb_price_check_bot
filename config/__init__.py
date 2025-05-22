"""
Пакет config.

Содержит константы и настройки, необходимые для работы бота.

Экспортируемые переменные:
    TOKEN (str): Токен Telegram-бота.
    PROJECT_PATH (str): Путь к корневой директории проекта.
    DB_CONN (list): Данные для подключения к БД.
    DEST (int): ID пункта выдачи заказов.
    CURRENCY (str): Обозначение валюты, в которой отображена стоимость книги.
"""

from config.constants import TOKEN
from config.constants import PROJECT_PATH
from config.constants import DB_CONN
from config.constants import DEST
from config.constants import CURRENCY
from config.constants import RABBIT_LOGIN
from config.constants import RABBIT_PASSWORD
