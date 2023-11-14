import os

import requests

from habits.models import Habit

TOKEN = os.getenv('TG_BOT_API_KEY')


def enable_notifications(obj: Habit, token=TOKEN) -> None:
    """
    Периодическая задача. Отправляет пользователю сообщение в телеграм с напоминанием о том, что пора выполнить привычку
    :param obj: Объект типа Habit
    :param token: API-токен чат-бота в телеграм
    :return: None
    """
    message = f'Пора выполнить привычку: {obj}' \
              f'Время на выполнение {obj.time_to_complete} секунд'

    send_message_url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={obj.user.chat_id}&text={message}"
    requests.get(send_message_url)
