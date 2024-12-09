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
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "cats_database"
COLLECTION_NAME = "cats"
