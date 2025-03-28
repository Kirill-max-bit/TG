from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_keyboard(
    *buttons: str,
    placeholder: str = "Выберите действие",
    request_contact: int = None,
    request_location: int = None,
    sizes: tuple[int] = (2,),
):
    """
    Создает кастомную клавиатуру для кино-бота

    Пример использования:
    get_movie_keyboard(
        "Фильмы",
        "Сериалы",
        "Мои рекомендации",
        "Настройки",
        "Помощь",
        placeholder="Что будем смотреть?",
        sizes=(2, 2, 1)
    )
    """
    kb_builder = ReplyKeyboardBuilder()

    for index, text in enumerate(buttons):
        if request_contact and request_contact == index:
            kb_builder.add(KeyboardButton(text=text, request_contact=True))
        elif request_location and request_location == index:
            kb_builder.add(KeyboardButton(text=text, request_location=True))
        else:
            kb_builder.add(KeyboardButton(text=text))

    return kb_builder.adjust(*sizes).as_markup(
        resize_keyboard=True,
        input_field_placeholder=placeholder
    )


# Примеры готовых клавиатур
def main_menu_kb():
    return get_keyboard(
        "🎬 Случайный фильм",
        "📺 Случайный сериал",
        "⭐ Избранное",
        "⚙ Настройки",
        sizes=(2, 1, 1)
    )


def genres_kb():
    return get_keyboard(
        "🍿 Комедии",
        "💥 Боевики",
        "👻 Ужасы",
        "💖 Мелодрамы",
        "🔍 Детективы",
        "◀ Назад",
        sizes=(2, 2, 2)
    )


def movie_control_kb():
    return get_keyboard(
        "👍 Нравится",
        "👎 Не нравится",
        "➕ В избранное",
        "🎲 Другой фильм",
        "📝 Описание",
        "◀ В меню",
        sizes=(3, 2, 1)
    )
