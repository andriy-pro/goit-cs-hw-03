from config import COLORS


def validate_name(name: str) -> tuple[bool, str]:
    """Валідація імені кота"""
    name = name.strip()
    if not name:
        return (
            False,
            f"{COLORS['error']}Ім'я кота не може бути порожнім!{COLORS['reset']}",
        )
    if len(name) < 2:
        return (
            False,
            f"{COLORS['error']}Ім'я кота має бути довшим за 1 символ!{COLORS['reset']}",
        )
    return True, name


def validate_age(age: str) -> tuple[bool, int, str]:
    """Валідація віку кота"""
    try:
        age_int = int(age)
        if age_int <= 0:
            return (
                False,
                0,
                f"{COLORS['error']}Вік кота має бути додатнім числом!{COLORS['reset']}",
            )
        if age_int > 30:
            return (
                False,
                0,
                f"{COLORS['warning']}Вказаний вік перевищує очікувану тривалість життя кота!{COLORS['reset']}",
            )
        return True, age_int, ""
    except ValueError:
        return False, 0, f"{COLORS['error']}Вік має бути цілим числом!{COLORS['reset']}"


def validate_features(features: str) -> tuple[bool, list, str]:
    """Валідація характеристик кота"""
    features_list = [f.strip() for f in features.split(",") if f.strip()]
    if not features_list:
        return (
            False,
            [],
            f"{COLORS['error']}Потрібно вказати хоча б одну характеристику!{COLORS['reset']}",
        )
    return True, features_list, ""
