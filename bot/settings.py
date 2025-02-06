from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",  # Указываем файл .env для загрузки переменных окружения
        env_file_encoding="utf-8",  # Кодировка файла .env
        extra="ignore",  # Игнорировать лишние поля
        case_sensitive=False  # Регистронезависимые переменные
    )

    # Обязательные поля
    tg_token: str = Field(..., alias="8030513880:AAGcG0LfcOnKKAluHPGEahV6CQ3IdUuq8cg")  # Токен Telegram-бота
    tg_timeout: int = Field(60 * 5, alias="TELEGRAM_TIMEOUT")  # Таймаут для Telegram
    kp_token: str = Field(..., alias="KP_TOKEN")  # Токен для Kinopoisk API
    kinoclub_token: str = Field(..., alias="KINOCLUB_TOKEN")  # Токен для Kinoclub API
    chat_url: str = Field(..., alias="CHAT_URL")  # Ссылка на канал
    chat_id: str = Field(..., alias="CHAT_ID")  # ID канала
    redis_dsn: str = Field("redis://localhost:6379")  # DSN для Redis


# Создаем экземпляр настроек
settings = Settings()
