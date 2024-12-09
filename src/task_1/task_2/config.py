import logging
import os
from datetime import datetime
from urllib.parse import urlparse

from colorama import Fore, Style

# MongoDB налаштування
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "cats_database")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "cats")
MONGO_TIMEOUT = 5000  # milliseconds

# Налаштування логування
LOG_DIR = "logs"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_LEVEL = logging.INFO

# Кольорові схеми для повідомлень
COLORS = {
    "success": Fore.GREEN,
    "warning": Fore.YELLOW,
    "error": Fore.RED,
    "header": Fore.CYAN,
    "reset": Style.RESET_ALL,
}

# Шаблони повідомлень
MESSAGES = {
    "menu_header": f"{COLORS['header']}=== МЕНЮ УПРАВЛІННЯ КОТЯЧОЮ БАЗОЮ ==={COLORS['reset']}",
    "cat_list_header": f"{COLORS['header']}=== Список усіх котів ==={COLORS['reset']}",
    "cat_list_footer": f"{COLORS['header']}=== Кінець списку ==={COLORS['reset']}",
    "empty_db": f"{COLORS['warning']}База даних порожня. Котів не знайдено.{COLORS['reset']}",
    "invalid_choice": f"{COLORS['warning']}Неправильний вибір. Спробуйте знову.{COLORS['reset']}",
    "exit": f"{COLORS['warning']}Вихід.{COLORS['reset']}",
}


def get_log_file():
    """Генерує шлях до файлу логу з часовою міткою"""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return os.path.join(LOG_DIR, f"cats_app_{timestamp}.log")


def setup_logging():
    """Налаштування системи логування"""
    logging.basicConfig(filename=get_log_file(), level=LOG_LEVEL, format=LOG_FORMAT)
    return logging.getLogger(__name__)


def validate_config():
    """Валідація конфігурації"""
    try:
        result = urlparse(MONGO_URI)
        if not all([result.scheme, result.netloc]):
            raise ValueError("Неправильний формат MONGO_URI")

        if not all([DATABASE_NAME, COLLECTION_NAME]):
            raise ValueError(
                "DATABASE_NAME та COLLECTION_NAME не можуть бути порожніми"
            )
    except Exception as e:
        raise ValueError(f"Помилка конфігурації: {e}")


# Валідація конфігурації при імпорті
validate_config()


def get_db_connection(uri: str, db_name: str, collection_name: str):
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.server_info()  # Перевірка з'єднання
        db = client[db_name]
        collection = db[collection_name]
        logger.info("Підключення до MongoDB успішне.")
        return collection
    except ServerSelectionTimeoutError as e:
        logger.error(f"Помилка підключення до MongoDB: {e}")
        raise
    except Exception as e:
        logger.error(f"Неочікувана помилка при підключенні до MongoDB: {e}")
        raise
