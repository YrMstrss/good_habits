import requests
import os

TOKEN = os.getenv('TG_BOT_API_KEY')


def get_chat_ids(token: str) -> dict:
    """
    Получает id чатов бота и имена пользователей телеграм
    :param token: строка с токеном тг-бота
    :return: словарь, где ключ - имя пользователя тг, а значение - id чата бота с данным пользователем
    """
    get_update_url = f"https://api.telegram.org/bot{token}/getUpdates"
    request = requests.get(get_update_url).json()
    if request['result']:
        bot_users = {}
        for result in request['result']:
            key = result['message']['chat']['username']
            value = result['message']['chat']['id']
            bot_users[key] = value
        return bot_users

    return {}
