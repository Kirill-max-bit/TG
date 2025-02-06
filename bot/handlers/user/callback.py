from pathlib import Path
import subprocess
import logging

from aiogram import Router, types, Bot

from bot.keyboards.inline import create_movie_buttons
from bot.handlers.user.search import kp_api
from bot.settings import settings
from bot.api import KinoClubAPI

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query()
async def process_callback(query: types.CallbackQuery, bot: Bot):
    data = query.data

    if data == 'pages:next_page':
        await next_page(query)
    elif data == 'pages:prev_page':
        await prev_page(query)
    elif data.startswith("movie:"):
        await process_movie_callback(query, bot)


async def next_page(query: types.CallbackQuery):
    logger.info("Обработчик next_page вызван")
    if kp_api.current_index + 10 < len(kp_api.results):
        kp_api.current_index += 10
        results = kp_api.results[kp_api.current_index:kp_api.current_index + 10]
        inline_kb = create_movie_buttons(results, kp_api.current_index, len(kp_api.results))
        await query.message.edit_text("Выберите фильм или сериал из списка ниже:", reply_markup=inline_kb)
        logger.info("Обработчик next_page обработал callback следующей страницы")


async def prev_page(query: types.CallbackQuery):
    logger.info("Обработчик prev_page вызван")
    if kp_api.current_index >= 10:
        kp_api.current_index -= 10
        results = kp_api.results[kp_api.current_index:kp_api.current_index + 10]
        inline_kb = create_movie_buttons(results, kp_api.current_index, len(kp_api.results))
        await query.message.edit_text("Выберите фильм или сериал из списка ниже:", reply_markup=inline_kb)
        logger.info("Обработчик prev_page обработал callback предыдущей страницы")


async def process_movie_callback(query: types.CallbackQuery, bot: Bot):
    logger.info("Обработчик process_movie_callback вызван")
    movie_id = query.data.split(":")[1]

    kinoclub_api = KinoClubAPI(settings.kinoclub_token)

    movie = await kinoclub_api.get_movie(movie_id)

    if movie is None:
        logger.error("Данные о фильме отсутствуют или не содержат ключ 'data'")
        await query.message.answer("Извините, информация о фильме не найдена.")
        return

    if movie.type == "film":
        # Отправить сообщение пользователю о начале процесса загрузки
        await query.message.answer("Начинаю загрузку видео...")

        tempfolder = Path("tempfiles").resolve()
        if not tempfolder.exists():
            tempfolder.mkdir(0o666, exist_ok=True)

        file_path = tempfolder / f"{movie_id}.mp4"
        # Загрузить и преобразовать файл
        try:
            process = subprocess.run([
                "yt-dlp", "--concurrent-fragments", "16", "--no-progress", "--user-agent",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36",
                "-o", str(file_path), str(movie.download_url)
            ])
            logger.info(f"YT-DLP exit: {process.returncode}")
        except Exception as ex:
            logger.info(str(ex))

        # Отправить файл пользователю
        await query.message.answer("Файл загружен, отправляю")
        logger.info(f"Files: {list(tempfolder.glob('*.*'))}")
        try:
            file = types.FSInputFile(path=file_path, filename=f"{movie.name}.mp4")
            file_id = await query.message.answer_video(video=file, supports_streaming=True)
            logger.info(f"FileID: {file_id}")
        except Exception as ex:
            logger.exception(str(ex))

        # Удалить временный файл
        file_path.unlink(missing_ok=True)

    elif movie.type == "serial":
        seasons_dict = {}
        for season in movie.seasons:
            series_dict = {}
            for seria in season.series:
                series_dict[seria.number] = seria.download_url
            seasons_dict[season.title] = series_dict

    message_text = f"<b>{movie.type.verbose}</b>: {movie.name}\\n\\n<b>Описание</b>:\\n{movie.full_description}"

    logger.info(
        f"Обработчик process_movie_callback отправил сообщение с информацией о '{movie.name}' (id:{movie.id})")
    await query.message.answer_photo(photo=str(movie.poster), caption=message_text, parse_mode="html")
