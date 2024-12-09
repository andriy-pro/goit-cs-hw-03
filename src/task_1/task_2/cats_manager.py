import logging

from config import COLORS
from pymongo.errors import PyMongoError
from validators import validate_age, validate_name

logger = logging.getLogger(__name__)


def show_all_cats(collection):
    try:
        cats = list(collection.find())
        if not cats:
            print(
                f"{COLORS['warning']}База даних порожня. Котів не знайдено.{COLORS['reset']}"
            )
            return
        print(f"\n{COLORS['info']}=== Список усіх котів ==={COLORS['reset']}")
        for i, cat in enumerate(cats, 1):
            print(f"\n{COLORS['success']}Кіт #{i}:{COLORS['reset']}")
            print(f"Ім'я: {cat.get('name', 'Невідомо')}")
            print(f"Вік: {cat.get('age', 'Невідомо')} років")
            print(f"Характеристики: {', '.join(cat.get('features', []))}")
        print(f"\n{COLORS['info']}=== Кінець списку ==={COLORS['reset']}")
        logger.info(f"Виведено {len(cats)} котів")
    except PyMongoError as e:
        logger.error(f"Помилка при отриманні списку котів: {e}")
        print(f"{COLORS['error']}Помилка при отриманні даних: {e}{COLORS['reset']}")


def find_cat_by_name(collection, name: str):
    if not name.strip():
        print(f"{COLORS['warning']}Ім'я кота не може бути порожнім!{COLORS['reset']}")
        return
    try:
        cat = collection.find_one({"name": name})
        if cat:
            print(f"\n{COLORS['success']}Знайдено кота:{COLORS['reset']}")
            print(f"Ім'я: {cat.get('name')}")
            print(f"Вік: {cat.get('age')} років")
            print(f"Характеристики: {', '.join(cat.get('features', []))}")
            logger.info(f"Знайдено кота: {name}")
        else:
            print(
                f"{COLORS['warning']}Кота з ім'ям '{name}' не знайдено.{COLORS['reset']}"
            )
            logger.warning(f"Кіт не знайдений: {name}")
    except PyMongoError as e:
        logger.error(f"Помилка пошуку кота: {e}")
        print(f"{COLORS['error']}Помилка пошуку: {e}{COLORS['reset']}")


def update_cat_age(collection, name: str, new_age: int):
    """Оновлює вік кота за його ім'ям."""
    is_valid, name_or_error = validate_name(name)
    if not is_valid:
        print(name_or_error)
        return

    is_valid, age_value, error = validate_age(str(new_age))
    if not is_valid:
        print(error)
        return

    try:
        result = collection.update_one({"name": name}, {"$set": {"age": age_value}})
        if result.modified_count > 0:
            print(
                f"{COLORS['success']}Вік кота з ім'ям {name} оновлено до {age_value} років.{COLORS['reset']}"
            )
            logger.info(f"Вік кота {name} оновлено до {age_value}.")
        else:
            print(
                f"{COLORS['warning']}Не вдалося оновити вік кота з ім'ям {name}.{COLORS['reset']}"
            )
            logger.warning(f"Оновлення віку кота {name} не вдалося.")
    except PyMongoError as e:
        logger.error(f"Помилка під час оновлення віку кота {name}: {e}")
        print(f"{COLORS['error']}Помилка оновлення: {e}{COLORS['reset']}")


def add_feature_to_cat(collection, name: str, feature: str):
    try:
        result = collection.update_one({"name": name}, {"$push": {"features": feature}})
        if result.modified_count > 0:
            print(
                f"{COLORS['success']}До характеристик кота з ім'ям {name} додано '{feature}'.{COLORS['reset']}"
            )
            logger.info(f"Характеристика '{feature}' додана коту {name}.")
        else:
            print(
                f"{COLORS['warning']}Не вдалося додати характеристику до кота {name}.{COLORS['reset']}"
            )
            logger.warning(f"Додавання характеристики до кота {name} не вдалося.")
    except PyMongoError as e:
        logger.error(f"Помилка під час додавання характеристики до кота {name}: {e}")
        print(
            f"{COLORS['error']}Помилка додавання характеристики: {e}{COLORS['reset']}"
        )


def delete_cat_by_name(collection, name: str):
    try:
        result = collection.delete_one({"name": name})
        if result.deleted_count > 0:
            print(f"{COLORS['success']}Кота з ім'ям {name} видалено.{COLORS['reset']}")
            logger.info(f"Кіт із ім'ям {name} видалений.")
        else:
            print(
                f"{COLORS['warning']}Не знайдено кота з ім'ям {name} для видалення.{COLORS['reset']}"
            )
            logger.warning(f"Видалення кота {name} не вдалося.")
    except PyMongoError as e:
        logger.error(f"Помилка під час видалення кота {name}: {e}")
        print(f"{COLORS['error']}Помилка видалення: {e}{COLORS['reset']}")


def delete_all_cats(collection):
    try:
        result = collection.delete_many({})
        print(
            f"{COLORS['success']}Усі коти видалені. Видалено {result.deleted_count} записів.{COLORS['reset']}"
        )
        logger.info(f"Усі коти видалені ({result.deleted_count} записів).")
    except PyMongoError as e:
        logger.error(f"Помилка під час видалення всіх котів: {e}")
        print(f"{COLORS['error']}Помилка видалення всіх котів: {e}{COLORS['reset']}")


def insert_cat(collection, name: str, age: int, features: list):
    try:
        cat_doc = {"name": name, "age": age, "features": features}
        inserted_id = collection.insert_one(cat_doc).inserted_id
        print(
            f"{COLORS['success']}Додано нового кота з ім'ям {name} (ID: {inserted_id}).{COLORS['reset']}"
        )
        logger.info(f"Новий кіт {name} (ID: {inserted_id}) доданий.")
    except PyMongoError as e:
        logger.error(f"Помилка під час додавання кота {name}: {e}")
        print(f"{COLORS['error']}Помилка додавання кота: {e}{COLORS['reset']}")
