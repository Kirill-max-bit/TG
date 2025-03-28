import os
import asyncio
from dotenv import load_dotenv
from loguru import logger
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from random import choice

load_dotenv()
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

MOVIES = [
    {
        "title": "Крестный отец",
        "year": 1972,
        "genre": "Криминал, Драма",
        "rating": 9.2
    },
    # ... остальные фильмы
]

SERIES = [
    {
        "title": "Игра престолов",
        "year": 2011,
        "genre": "Фэнтези, Драма",
        "seasons": 8
    },
    # ... остальные сериалы
]


async def send_recommendation(bot: Bot):
    while True:
        try:
            item = choice(MOVIES) if choice([True, False]) else choice(SERIES)

            if 'rating' in item:
                message = (
                    "🎬 <b>Фильм для просмотра:</b>\n"
                    f"<b>Название:</b> {item['title']}\n"
                    f"<b>Год:</b> {item['year']}\n"
                    f"<b>Жанр:</b> {item['genre']}\n"
                    f"<b>Рейтинг:</b> ⭐ {item['rating']}/10"
                )
            else:
                message = (
                    "📺 <b>Сериал для просмотра:</b>\n"
                    f"<b>Название:</b> {item['title']}\n"
                    f"<b>Год:</b> {item['year']}\n"
                    f"<b>Жанр:</b> {item['genre']}\n"
                    f"<b>Сезонов:</b> {item['seasons']}"
                )

            await bot.send_message(
                chat_id=CHANNEL_ID,
                text=message,
                parse_mode="HTML"
            )
            logger.info(f"Отправлена рекомендация: {item['title']}")

        except Exception as e:
            logger.error(f"Ошибка при отправке: {str(e)}")
            await asyncio.sleep(60)  # Пауза при ошибке

        await asyncio.sleep(3600)  # Основная пауза


async def main():
    logger.add(
        "film_bot.log",
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
        rotation="1 week"
    )

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    @dp.message(Command("start"))
    async def start_handler(message: types.Message):
        await message.answer("Бот кинопоиска запущен!")

    task = asyncio.create_task(send_recommendation(bot))

    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка в основном цикле: {e}")
    finally:
        task.cancel()
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
