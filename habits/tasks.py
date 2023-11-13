import requests
import os

TOKEN = os.getenv('TG_BOT_API_KEY')


def get_chat_ids(token: str) -> list:
    """Получает id чатов бота"""
    get_update_url = f"https://api.telegram.org/bot{token}/getUpdates"
    request = requests.get(get_update_url).json()
    if request['result']:
        chat_ids = []
        for result in request['result']:
            chat_ids.append(result['message']['chat']['id'])
        return chat_ids

    return []
