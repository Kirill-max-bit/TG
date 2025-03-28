from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove


admin_router = Router()
admin_router.message.filter(F.chat.type == "private")


MOVIES = [
    {"title": "Пример фильма", "year": "2023", "genre": "Драма", "rating": 8.5}
]


ADMIN_KB = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="Добавить фильм")],
        [types.KeyboardButton(text="Удалить фильм")],
        [types.KeyboardButton(text="Список контента")],
        [types.KeyboardButton(text="Статистика")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие"
)


class AddMovie(StatesGroup):
    title = State()
    year = State()
    genre = State()
    rating = State()
    description = State()
    image = State()


@admin_router.message(Command("admin"))
async def admin_panel(message: types.Message):
    """Главное меню админ-панели"""
    await message.answer(
        "Админ-панель управления контентом:",
        reply_markup=ADMIN_KB
    )


@admin_router.message(F.text == "Добавить фильм")
async def add_movie_start(message: types.Message, state: FSMContext):
    """Начало процесса добавления фильма"""
    await message.answer(
        "Введите название фильма:",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(AddMovie.title)


@admin_router.message(AddMovie.title)
async def add_movie_title(message: types.Message, state: FSMContext):
    """Обработка названия фильма"""
    await state.update_data(title=message.text)
    await message.answer("Введите год выпуска:")
    await state.set_state(AddMovie.year)


@admin_router.message(AddMovie.year)
async def add_movie_year(message: types.Message, state: FSMContext):
    """Обработка года выпуска"""
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите корректный год цифрами:")
        return

    await state.update_data(year=message.text)
    await message.answer("Введите жанры (через запятую):")
    await state.set_state(AddMovie.genre)


@admin_router.message(AddMovie.genre)
async def add_movie_genre(message: types.Message, state: FSMContext):
    """Обработка жанров"""
    await state.update_data(genre=message.text)
    await message.answer("Введите рейтинг (например 8.5):")
    await state.set_state(AddMovie.rating)


@admin_router.message(AddMovie.rating)
async def add_movie_rating(message: types.Message, state: FSMContext):
    """Обработка рейтинга"""
    try:
        rating = float(message.text)
        if rating < 0 or rating > 10:
            raise ValueError
    except ValueError:
        await message.answer("Введите число от 0 до 10 (напр. 7.8):")
        return

    await state.update_data(rating=str(rating))
    await message.answer("Введите описание фильма:")
    await state.set_state(AddMovie.description)


@admin_router.message(AddMovie.description)
async def add_movie_description(message: types.Message, state: FSMContext):
    """Обработка описания"""
    await state.update_data(description=message.text)
    await message.answer("Загрузите постер фильма:")
    await state.set_state(AddMovie.image)


@admin_router.message(AddMovie.image, F.photo)
async def add_movie_image(message: types.Message, state: FSMContext):
    """Обработка постера фильма"""
    photo = message.photo[-1]
    photo_id = photo.file_id

    data = await state.get_data()

    new_movie = {
        "title": data["title"],
        "year": data["year"],
        "genre": data["genre"],
        "rating": float(data["rating"]),
        "description": data["description"],
        "image": photo_id
    }
    MOVIES.append(new_movie)

    await message.answer(
        f"Фильм добавлен!\n\n"
        f"Название: {data['title']}\n"
        f"Год: {data['year']}\n"
        f"Жанр: {data['genre']}\n"
        f"Рейтинг: {data['rating']}\n"
        f"Описание: {data['description']}",
        reply_markup=ADMIN_KB
    )
    await state.clear()


@admin_router.message(F.text == "Список контента")
async def list_content(message: types.Message):
    """Показ списка фильмов"""
    response = "Список фильмов:\n\n"
    for i, movie in enumerate(MOVIES, 1):
        response += f"{i}. {movie['title']} ({movie['year']})\n"

    await message.answer(response or "База данных пуста")


@admin_router.message(F.text == "Удалить фильм")
async def delete_movie_start(message: types.Message):
    """Начало процесса удаления фильма"""
    await message.answer(
        "Функция удаления в разработке. "
        "Будет реализована через inline-кнопки",
        reply_markup=ADMIN_KB
    )


@admin_router.message(F.text == "Статистика")
async def show_stats(message: types.Message):
    """Показ статистики"""
    await message.answer(
        "Статистика бота:\n"
        f"Фильмов в базе: {len(MOVIES)}\n"
        "Сериалов в базе: 0\n"
        "Всего рекомендаций отправлено: 0",
        reply_markup=ADMIN_KB
    )


@admin_router.message(Command("отмена"))
@admin_router.message(F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext):
    """Отмена текущего действия"""
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(
        "Действия отменены",
        reply_markup=ADMIN_KB
    )
