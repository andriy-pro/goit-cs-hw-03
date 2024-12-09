from cats_manager import (
    add_feature_to_cat,
    delete_all_cats,
    delete_cat_by_name,
    find_cat_by_name,
    insert_cat,
    show_all_cats,
    update_cat_age,
)
from colorama import init
from config import (
    COLLECTION_NAME,
    COLORS,
    DATABASE_NAME,
    MESSAGES,
    MONGO_URI,
    setup_logging,
)
from db_connection import get_db_connection
from validators import validate_age, validate_features, validate_name

# Ініціалізація colorama
init()

# Налаштування логування
logger = setup_logging()


def main_menu(collection):
    while True:
        print(f"\n{MESSAGES['menu_header']}")
        print("1. Показати всіх котів")
        print("2. Знайти кота за ім'ям")
        print("3. Оновити вік кота")
        print("4. Додати характеристику до кота")
        print("5. Видалити кота за ім'ям")
        print("6. Видалити всіх котів")
        print("7. Додати нового кота")
        print(f"{COLORS['error']}0. Вийти{COLORS['reset']}")

        try:
            choice = input(f"{COLORS['success']}Оберіть опцію: {COLORS['reset']}")
            if choice == "1":
                show_all_cats(collection)
            elif choice == "2":
                name = input("Введіть ім'я кота: ")
                is_valid, name_or_error = validate_name(name)
                if not is_valid:
                    print(name_or_error)
                    continue
                find_cat_by_name(collection, name_or_error)
            elif choice == "3":
                name = input("Введіть ім'я кота: ")
                is_valid, name_or_error = validate_name(name)
                if not is_valid:
                    print(name_or_error)
                    continue

                age = input("Введіть новий вік кота: ")
                is_valid, age_value, error = validate_age(age)
                if not is_valid:
                    print(error)
                    continue

                update_cat_age(collection, name_or_error, age_value)
            elif choice == "4":
                name = input("Введіть ім'я кота: ")
                feature = input("Введіть нову характеристику: ")
                add_feature_to_cat(collection, name, feature)
            elif choice == "5":
                name = input("Введіть ім'я кота: ")
                delete_cat_by_name(collection, name)
            elif choice == "6":
                delete_all_cats(collection)
            elif choice == "7":
                name = input("Введіть ім'я кота: ")
                is_valid, name_or_error = validate_name(name)
                if not is_valid:
                    print(name_or_error)
                    continue

                age = input("Введіть вік кота: ")
                is_valid, age_value, error = validate_age(age)
                if not is_valid:
                    print(error)
                    continue

                features_input = input("Введіть характеристики (через кому): ")
                is_valid, features_list, error = validate_features(features_input)
                if not is_valid:
                    print(error)
                    continue

                insert_cat(collection, name_or_error, age_value, features_list)
            elif choice == "0":
                print("Вихід.")
                break
            else:
                print("Неправильний вибір. Спробуйте знову.")
        except ValueError as e:
            print(f"{COLORS['error']}Помилка введення: введіть число!{COLORS['reset']}")
            continue
        except Exception as e:
            print(f"{COLORS['error']}Неочікувана помилка: {e}{COLORS['reset']}")
            logger.error(f"Помилка в головному меню: {e}")
            continue


if __name__ == "__main__":
    collection = get_db_connection(MONGO_URI, DATABASE_NAME, COLLECTION_NAME)
    main_menu(collection)
