import os

import requests

from habits.models import Habit

TOKEN = os.getenv('TG_BOT_API_KEY')


def enable_notifications(obj: Habit, token=TOKEN):
    """
    Периодическая задача. Отправляет пользователю сообщение в телеграм с напоминанием о том, что пора выполнить привычку
    """
    message = f'Пора выполнить привычку: {obj}' \
              f'Время на выполнение {obj.time_to_complete} секунд'

    send_message_url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={obj.user.chat_id}&text={message}"
    requests.get(send_message_url)
