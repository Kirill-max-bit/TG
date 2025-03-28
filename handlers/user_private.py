from loguru import logger
from aiogram import F
from aiogram import types
from aiogram import Router
from aiogram.filters import CommandStart, Command, or_f
from aiogram.utils.formatting import as_list, as_marked_section, Bold
from filters.chat_types import ChatTypeFilter
from kbdn.reply import get_keyboard

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    logger.info(
        'Пользователь %s запустил кино-бота',
        message.from_user.full_name
    )

    welcome_text = as_list(
        Bold(f"Привет, {message.from_user.full_name}!"),
        "Я - твой персональный кино-бот 🎬",
        "Я помогу:",
        as_marked_section(
            "• Найти фильмы по жанру/году/рейтингу",
            "• Посоветовать что посмотреть",
            "• Сохранить твою коллекцию фильмов",
            marker="✅ "
        )
    )

    await message.answer(**welcome_text.as_kwargs())

    await message.answer(
        "Выбери действие:",
        reply_markup=get_keyboard(
            "Поиск фильмов",
            "Рекомендации",
            "Моя коллекция",
            "Топ фильмов",
            placeholder="Что хочешь сделать?",
            sizes=(2, 2)
        ),
    )


search_filter = or_f(
    Command("search"),
    (F.text.lower() == "поиск фильмов")
)


@user_private_router.message(search_filter)
async def search_films(message: types.Message):
    await message.answer(
        "Искать фильмы по:",
        reply_markup=get_keyboard(
            "По жанру",
            "По году",
            "По рейтингу",
            "По актерам",
            "Назад",
            placeholder="Выбери критерий поиска",
            sizes=(2, 2, 1)
        ),
    )


@user_private_router.message(
    or_f(
        Command("recommend"),
        (F.text.lower() == "рекомендации")
    )
)
async def recommend_films(message: types.Message):
    await message.answer(
        "Выбери тип рекомендаций:",
        reply_markup=get_keyboard(
            "По любимым жанрам",
            "Похожие на...",
            "Случайный фильм",
            "Назад",
            placeholder="Как искать?",
            sizes=(2, 1, 1)
        ),
    )


collection_filter = or_f(
    Command("collection"),
    (F.text.lower() == "моя коллекция")
)


@user_private_router.message(collection_filter)
async def show_collection(message: types.Message):
    await message.answer(
        "Твоя коллекция фильмов:",
        reply_markup=get_keyboard(
            "Просмотр коллекции",
            "Добавить фильм",
            "Удалить фильм",
            "Назад",
            placeholder="Управление коллекцией",
            sizes=(2, 1, 1)
        ),
    )


top_filter = or_f(
    Command("top"),
    (F.text.lower() == "топ фильмов")
)


@user_private_router.message(top_filter)
async def show_top(message: types.Message):
    await message.answer(
        "Топ фильмов по:",
        reply_markup=get_keyboard(
            "IMDb",
            "Кинопоиску",
            "Оскар 2024",
            "Золотая малина",
            "Назад",
            placeholder="Выбери рейтинг",
            sizes=(2, 2, 1)
        ),
    )


@user_private_router.message(F.text.lower() == "назад")
async def back_handler(message: types.Message):
    await start_cmd(message)
