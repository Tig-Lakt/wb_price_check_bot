import os
import sys

import yaml
import logging
from dotenv import load_dotenv

# Добавляем корневой каталог проекта в PYTHONPATH для удобства импорта
PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_PATH)

# Загружаем переменные окружения из файла .env
dotenv_path = os.path.join(PROJECT_PATH, ".env")  # Путь к файлу .env
load_dotenv(dotenv_path, override=True)  # Загружает переменные окружения из .env в os.environ

CONFIG_FILE_PATH = os.path.join(PROJECT_PATH, "src", "config.yaml")

logging.basicConfig(level=logging.INFO)


def get_bot_token() -> str:
    """
    Получает токен бота из переменной окружения TELEGRAM_BOT_TOKEN.

    Returns:
        str: Токен бота.
    """
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    print(token, '111')
    if not token:
        logging.error("Ошибка: Переменная окружения TELEGRAM_BOT_TOKEN не задана.")
        return None  # Или raise EnvironmentError

    return token


def update_config_file(token: str=None, host: str=None, port: int=None, database: str=None, user: str=None, password: str=None):
    print(token, 'update_config_file')
    """
    Обновляет config.yaml с токеном бота и/или параметрами базы данных.

    Args:
        token (str): Токен бота.
        host (str, optional): Хост базы данных. Defaults to None.
        port (int, optional): Порт базы данных. Defaults to None.
        database (str, optional): Имя базы данных. Defaults to None.
        user (str, optional): Имя пользователя базы данных. Defaults to None.
        password (str, optional): Пароль базы данных. Defaults to None.
    """
    config_data = {"bot_token": token}
    print(config_data, 'config_data')

    if host is not None: 
        config_data["host"] = host
        config_data["port"] = port
        config_data["database"] = database
        config_data["user"] = user
        config_data["password"] = password

    try:
        with open(CONFIG_FILE_PATH, "w") as file:
            yaml.dump(config_data, file)
    except Exception as e:
        logging.error(f"Ошибка при записи в config.yaml: {e}")


def get_db_connection_params() -> list[str]:
    """
    Извлекает параметры подключения к базе данных из файла конфигурации.

    Returns:
        list[str]: Список параметров подключения [host, port, database, user, password].
    """
    try:
        with open(CONFIG_FILE_PATH, "r") as file:
            config = yaml.safe_load(file)
            host = os.environ.get("DB_HOST") or config.get("host")
            port = os.environ.get("DB_PORT") or config.get("port")
            database = os.environ.get("DB_NAME") or config.get("database")
            user = os.environ.get("DB_USER") or config.get("user")
            password = os.environ.get("DB_PASSWORD") or config.get("password")

            return [host, port, database, user, password]
    except FileNotFoundError:
        print(f"Ошибка: Файл конфигурации не найден: {CONFIG_FILE_PATH}")
        return []
    except KeyError as e:
        print(f"Ошибка: Ключ '{e}' отсутствует в файле конфигурации.")
        return []
    except yaml.YAMLError as e:
        print(f"Ошибка: Ошибка при чтении YAML файла: {e}")
        return []
