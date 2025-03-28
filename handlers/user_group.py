import asyncio
from string import punctuation
from typing import Dict, Set

from aiogram import Bot, types, Router
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest
from filters.chat_types import ChatTypeFilter
from common.restricted_words import restricted_words


user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(["group", "supergroup"]))
user_group_router.edited_message.filter(ChatTypeFilter(["group", "super"]))


WARNING_MESSAGE = " соблюдайте порядок в чате!"


class ChatCleaner:
    """Utility class for chat message processing"""

    @staticmethod
    def clean_text(text: str) -> str:
        """Remove punctuation and return cleaned text"""
        if not isinstance(text, str):
            return ""
        return text.translate(str.maketrans("", "", punctuation)).lower()

    @staticmethod
    def has_restricted_words(text: str, restricted: Set[str]) -> bool:
        """Check if text contains restricted words"""
        if not text:
            return False
        cleaned_text = ChatCleaner.clean_text(text)
        return bool(restricted.intersection(cleaned_text.split()))


chat_admins: Dict[int, Set[int]] = {}


@user_group_router.message(Command("admin"))
async def handle_admin_command(message: types.Message, bot: Bot) -> None:
    """
    Обработчик команды /admin
    Получает список администраторов чата и сохраняет их ID
    """
    try:
        chat_id = message.chat.id
        admins = await fetch_chat_admins(bot, chat_id)

        if message.from_user.id in admins:
            chat_admins[chat_id] = admins
            await message.delete()
        else:
            await message.answer
            ("⚠️ Только администраторы могут использовать эту команду")

    except TelegramBadRequest:
        await message.answer
        ("❌ Ошибка: недостаточно прав для получения списка администраторов")
    except Exception as e:
        await message.answer(f"⚠️ Произошла ошибка: {str(e)}")


async def fetch_chat_admins(bot: Bot, chat_id: int) -> Set[int]:
    """Получает список ID администраторов чата"""
    admins_list = await bot.get_chat_administrators(chat_id)
    return {
        member.user.id
        for member in admins_list
        if member.status in ("creator", "administrator")
    }


@user_group_router.message()
@user_group_router.edited_message()
async def cleaner(message: types.Message) -> None:
    """Check messages for restricted words"""
    try:
        if not message.text:
            return

        if ChatCleaner.has_restricted_words(message.text, restricted_words):
            # Оптимизированная проверка прав
            if message.from_user.id in chat_admins.get(message.chat.id, set()):
                return  # Пропускаем админов

            user_name = message.from_user.first_name
            warning = await message.answer(f"{user_name},{WARNING_MESSAGE}")
            await message.delete()

            await asyncio.sleep(5)
            try:
                await warning.delete()
            except TelegramBadRequest:
                pass

    except TelegramBadRequest:
        print("Не удалось удалить сообщение")
    except Exception as e:
        print(f"Ошибка: {e}")


def is_user_admin(chat_id: int, user_id: int) -> bool:
    """Проверяет, является ли пользователь админом чата"""
    return user_id in chat_admins.get(chat_id, set())


@user_group_router.message(Command("check_admin"))
async def check_admin_status(message: types.Message) -> None:
    try:
        status = (
            "администратор"
            if is_user_admin(message.chat.id, message.from_user.id)
            else "не администратор"
        )
        await message.answer(f"Вы {status} чата!")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")
