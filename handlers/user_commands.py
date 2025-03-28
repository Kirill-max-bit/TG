from aiogram import Dispatcher, types
from aiogram.exceptions import TelegramBadRequest
from loguru import logger


def register_error_handlers(dp: Dispatcher):
    @dp.errors_handler(exception=TelegramBadRequest)
    async def telegram_error_handler(
        update: types.Update,
        exception: TelegramBadRequest
    ):
        if "chat not found" in str(exception):
            logger.error("Чат не найден!")
        return True
