import logging

from colorama import Fore, Style, init
from config import COLLECTION_NAME, DATABASE_NAME, MONGO_URI
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

# Ініціалізація colorama
init()

# Налаштування логування
logging.basicConfig(
    filename="cats_app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Підключення до MongoDB
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.server_info()  # Перевірка з'єднання
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    logger.info("Підключення до MongoDB успішно.")
except ServerSelectionTimeoutError as e:
    logger.error(f"Помилка підключення до MongoDB: {e}")
    print(
        f"{Fore.RED}Помилка підключення до бази даних. Перевірте, чи запущено MongoDB.{Style.RESET_ALL}"
    )
    raise
except Exception as e:
    logger.error(f"Неочікувана помилка при підключенні до MongoDB: {e}")
    raise


def show_all_cats():
    try:
        cats = list(collection.find())
        if not cats:
            print(
                f"{Fore.YELLOW}База даних порожня. Котів не знайдено.{Style.RESET_ALL}"
            )
            return

        print(f"\n{Fore.CYAN}=== Список усіх котів ==={Style.RESET_ALL}")
        for i, cat in enumerate(cats, 1):
            print(f"\n{Fore.GREEN}Кіт #{i}:{Style.RESET_ALL}")
            print(f"Ім'я: {cat.get('name', 'Невідомо')}")
            print(f"Вік: {cat.get('age', 'Невідомо')} років")
            print(f"Характеристики: {', '.join(cat.get('features', []))}")
        print(f"\n{Fore.CYAN}=== Кінець списку ==={Style.RESET_ALL}")
        logger.info(f"Виведено {len(cats)} котів")
    except Exception as e:
        logger.error(f"Помилка при отриманні списку котів: {e}")
        print(f"{Fore.RED}Помилка при отриманні даних: {e}{Style.RESET_ALL}")


def find_cat_by_name(name: str):
    if not name.strip():
        print(f"{Fore.YELLOW}Ім'я кота не може бути порожнім!{Style.RESET_ALL}")
        return

    try:
        cat = collection.find_one({"name": name})
        if cat:
            print(f"\n{Fore.GREEN}Знайдено кота:{Style.RESET_ALL}")
            print(f"Ім'я: {cat.get('name')}")
            print(f"Вік: {cat.get('age')} років")
            print(f"Характеристики: {', '.join(cat.get('features', []))}")
            logger.info(f"Знайдено кота: {name}")
        else:
            print(f"{Fore.YELLOW}Кота з ім'ям '{name}' не знайдено.{Style.RESET_ALL}")
            logger.warning(f"Кіт не знайдений: {name}")
    except Exception as e:
        logger.error(f"Помилка пошуку кота: {e}")
        print(f"{Fore.RED}Помилка пошуку: {e}{Style.RESET_ALL}")


def update_cat_age(name: str, new_age: int):
    """
    Оновлює вік кота за його ім'ям.
    :param name: Ім'я кота.
    :param new_age: Новий вік кота.
    """
    try:
        result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.modified_count > 0:
            print(f"Вік кота з ім'ям {name} оновлено до {new_age} років.")
            logger.info(f"Вік кота {name} оновлено до {new_age}.")
        else:
            print(f"Не вдалося оновити вік кота з ім'ям {name}.")
            logger.warning(f"Оновлення віку кота {name} не вдалося.")
    except Exception as e:
        logger.error(f"Помилка під час оновлення віку кота {name}: {e}")


def add_feature_to_cat(name: str, feature: str):
    """
    Додає нову характеристику до списку 'features' кота за його ім'ям.
    :param name: Ім'я кота.
    :param feature: Нова характеристика для додавання.
    """
    try:
        result = collection.update_one({"name": name}, {"$push": {"features": feature}})
        if result.modified_count > 0:
            print(f"До характеристик кота з ім'ям {name} додано '{feature}'.")
            logger.info(f"Характеристика '{feature}' додана коту {name}.")
        else:
            print(f"Не вдалося додати характеристику до кота {name}.")
            logger.warning(f"Додавання характеристики до кота {name} не вдалося.")
    except Exception as e:
        logger.error(f"Помилка під час додавання характеристики до кота {name}: {e}")


def delete_cat_by_name(name: str):
    """
    Видаляє кота з колекції за його ім'ям.
    :param name: Ім'я кота, якого потрібно видалити.
    """
    try:
        result = collection.delete_one({"name": name})
        if result.deleted_count > 0:
            print(f"Кота з ім'ям {name} видалено.")
            logger.info(f"Кіт із ім'ям {name} видалений.")
        else:
            print(f"Не знайдено кота з ім'ям {name} для видалення.")
            logger.warning(f"Видалення кота {name} не вдалося.")
    except Exception as e:
        logger.error(f"Помилка під час видалення кота {name}: {e}")


def delete_all_cats():
    """
    Видаляє всі записи з колекції.
    Увага: Ця операція незворотна!
    """
    try:
        result = collection.delete_many({})
        print(f"Усі коти видалені. Видалено {result.deleted_count} записів.")
        logger.info(f"Усі коти видалені ({result.deleted_count} записів).")
    except Exception as e:
        logger.error(f"Помилка під час видалення всіх котів: {e}")


def insert_cat(name: str, age: int, features: list):
    """
    Створює новий запис (документ) у колекції.
    :param name: Ім'я кота.
    :param age: Вік кота.
    :param features: Список характеристик кота.
    """
    try:
        cat_doc = {"name": name, "age": age, "features": features}
        inserted_id = collection.insert_one(cat_doc).inserted_id
        print(f"Додано нового кота з ім'ям {name} (ID: {inserted_id}).")
        logger.info(f"Новий кіт {name} (ID: {inserted_id}) доданий.")
    except Exception as e:
        logger.error(f"Помилка під час додавання кота {name}: {e}")


def main_menu():
    while True:
        print(f"\n{Fore.CYAN}=== МЕНЮ УПРАВЛІННЯ КОТЯЧОЮ БАЗОЮ ==={Style.RESET_ALL}")
        print("1. Показати всіх котів")
        print("2. Знайти кота за ім'ям")
        print("3. Оновити вік кота")
        print("4. Додати характеристику до кота")
        print("5. Видалити кота за ім'ям")
        print("6. Видалити всіх котів")
        print("7. Додати нового кота")
        print(f"{Fore.RED}0. Вийти{Style.RESET_ALL}")

        try:
            choice = input(f"{Fore.GREEN}Оберіть опцію: {Style.RESET_ALL}")
            if choice == "1":
                show_all_cats()
            elif choice == "2":
                name = input("Введіть ім'я кота: ")
                find_cat_by_name(name)
            elif choice == "3":
                name = input("Введіть ім'я кота: ")
                new_age = int(input("Введіть новий вік кота: "))
                update_cat_age(name, new_age)
            elif choice == "4":
                name = input("Введіть ім'я кота: ")
                feature = input("Введіть нову характеристику: ")
                add_feature_to_cat(name, feature)
            elif choice == "5":
                name = input("Введіть ім'я кота: ")
                delete_cat_by_name(name)
            elif choice == "6":
                delete_all_cats()
            elif choice == "7":
                name = input("Введіть ім'я кота: ")
                age = int(input("Введіть вік кота: "))
                features = input("Введіть характеристики (через кому): ").split(", ")
                insert_cat(name, age, features)
            elif choice == "0":
                print("Вихід.")
                break
            else:
                print("Неправильний вибір. Спробуйте знову.")
        except ValueError as e:
            print(f"{Fore.RED}Помилка введення: введіть число!{Style.RESET_ALL}")
            continue
        except Exception as e:
            print(f"{Fore.RED}Неочікувана помилка: {e}{Style.RESET_ALL}")
            logger.error(f"Помилка в головному меню: {e}")
            continue


if __name__ == "__main__":
    main_menu()
