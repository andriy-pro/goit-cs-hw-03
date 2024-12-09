from config import MONGO_TIMEOUT, setup_logging
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

logger = setup_logging()


def get_db_connection(uri: str, db_name: str, collection_name: str):
    if not all([uri, db_name, collection_name]):
        raise ValueError("URI, назва бази даних та колекції не можуть бути порожніми")

    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=MONGO_TIMEOUT)
        client.server_info()
        db = client[db_name]
        collection = db[collection_name]
        logger.info(
            f"Підключення до MongoDB успішне. БД: {db_name}, Колекція: {collection_name}"
        )
        return collection
    except ServerSelectionTimeoutError as e:
        logger.error(f"Помилка підключення до MongoDB: {e}")
        raise
    except Exception as e:
        logger.error(f"Неочікувана помилка при підключенні до MongoDB: {e}")
        raise
