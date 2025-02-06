from celery import Celery
from bot.settings import settings

# Инициализация Celery с использованием Redis в качестве брокера
job_queue = Celery("bot", broker=settings.redis_dsn)

# Настройка Celery (опционально)
job_queue.conf.update(
    result_backend=settings.redis_dsn,  # Используем Redis для хранения результатов
    task_serializer="json",  # Сериализация задач в JSON
    accept_content=["json"],  # Принимаем только JSON
    result_serializer="json",  # Сериализация результатов в JSON
    timezone="Europe/Moscow",  # Часовой пояс
    enable_utc=True,  # Использовать UTC
)
