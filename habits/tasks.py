import os

import requests

from habits.models import Habit

TOKEN = os.getenv('TG_BOT_API_KEY')


def enable_notifications_task(pk: int, token=TOKEN) -> None:
    """
    Периодическая задача. Отправляет пользователю сообщение в телеграм с напоминанием о том, что пора выполнить привычку
    :param pk: ID привычки
    :param token: API-токен чат-бота в телеграм
    :return: None
    """
    obj = Habit.objects.get(pk=pk)

    message = f'Пора выполнить привычку: {obj}\nВремя на выполнение {obj.time_to_complete} секунд'

    send_message_url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={obj.user.chat_id}&text={message}"
    requests.get(send_message_url)
