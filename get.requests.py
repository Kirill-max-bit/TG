import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


def get_movie_data(query):
    url = 'https://kinopoiskapiunofficial.tech/api/v2.2/films'
    headers = {
        'X-API-KEY': 'TOKEN_KP',  # Ваш ключ
        'Content-Type': 'application/json'
    }
    params = {'keyword': query}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get('items', [])
    except requests.exceptions.RequestException as e:
        return f"Ошибка при запросе: {e}"
