from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from loguru import logger

ADMIN_CHAT_ID = "@Splash_786"


async def handle_telegram_error(bot: Bot, channel_id: int, e: Exception):
    """
    Обработчик ошибок Telegram для канала

    :param bot: Экземпляр бота
    :param channel_id: ID канала, где произошла ошибка
    :param e: Исключение
    """
    if isinstance(e, TelegramBadRequest):
        if "chat not found" in str(e):
            logger.error(f"Канал {channel_id} не найден")
            try:
                await bot.send_message(
                    chat_id=ADMIN_CHAT_ID,
                    text=f"Ошибка доступа к каналу: {channel_id}"
                )
            except Exception as admin_error:
                logger.error(f"Не удалось уведомить админа: {admin_error}")
