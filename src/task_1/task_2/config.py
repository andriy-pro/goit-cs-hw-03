import os
from urllib.parse import urlparse

# Запуск MongoDB в Docker
# docker run --name mongodb -p 27017:27017 -d mongo
# --name mongodb: назва контейнера
# -p 27017:27017: прослуховування порту 27017 на хості та перенаправлення його у контейнер
# -d mongo: запуск MongoDB у фоновому режимі з використанням офіційного образу mongo з Docker Hub.
#
# Перевірка роботи:
# docker ps
# (в списку контейнерів повинен бути контейнер з назвою 'mongodb')


# Налаштування для підключення до MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "cats_database")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "cats")

# Валідація URI
try:
    result = urlparse(MONGO_URI)
    if not all([result.scheme, result.netloc]):
        raise ValueError("Неправильний формат MONGO_URI")
except Exception as e:
    raise ValueError(f"Помилка конфігурації MONGO_URI: {e}")

# Валідація імен бази даних та колекції
if not all([DATABASE_NAME, COLLECTION_NAME]):
    raise ValueError("DATABASE_NAME та COLLECTION_NAME не можуть бути порожніми")
