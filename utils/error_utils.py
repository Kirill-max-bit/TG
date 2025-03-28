from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from loguru import logger


ADMIN_CHAT_ID = 123456789


async def handle_telegram_error(bot: Bot, chat_id: int, e: Exception):
    """
    Обработчик ошибок Telegram

    :param bot: Экземпляр бота
    :param chat_id: ID чата, где произошла ошибка
    :param e: Исключение
    """
    if isinstance(e, TelegramBadRequest):
        if "chat not found" in str(e):
            logger.error(f"Чат {chat_id} не найден")
            try:
                await bot.send_message(
                    chat_id=ADMIN_CHAT_ID,
                    text=f"Ошибка доступа к чату: {chat_id}"
                )
            except Exception as admin_error:
                logger.error(f"Не удалось уведомить админа: {admin_error}")
