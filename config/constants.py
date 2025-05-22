"""
Модуль config.constants

Содержит константы и настройки, используемые в проекте, такие как токен бота,
данные подключения к PostgreSQL.
"""

import os
import sys
from utils import get_bot_token, get_db_connection_params, update_config_file


update_config_file()

# Получаем абсолютный путь к корневой директории проекта.
# Используем os.path.dirname(__file__) для получения пути к текущему файлу (constants.py),
# затем переходим на один уровень выше, чтобы получить путь к PROJECT_PATH.
PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Добавляем путь к проекту в sys.path, чтобы можно было импортировать модули из проекта.
sys.path.insert(0, PROJECT_PATH)

# Получаем токен бота из переменной окружения или файла конфигурации (см. utils.py).
TOKEN = get_bot_token()
print(TOKEN, 'TOKEN')

# Получаем данные подключения к базе данных из переменной окружения или файла конфигурации (см. utils.py).
DB_CONN = get_db_connection_params()

CURRENCY = 'rub'
DEST = '-1255942'

#
RABBIT_LOGIN = "guest"
RABBIT_PASSWORD = "guest"