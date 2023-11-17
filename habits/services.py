import json
from datetime import datetime, timedelta

from django_celery_beat.models import PeriodicTask, \
    IntervalSchedule

from habits.models import Habit


def create_periodic_task(obj: Habit) -> None:
    """
    Функция, создающая периодическую задачу по данным модели привычки
    :param obj: Объект класса Habit
    :return: None
    """
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=int(obj.period),
        period=IntervalSchedule.DAYS,
    )

    if datetime.now().time() < obj.time:
        start_time = datetime.combine(datetime.today(), obj.time)
    else:
        start_time = datetime.combine(datetime.today() + timedelta(days=1), obj.time)

    PeriodicTask.objects.create(
        interval=schedule,
        name=obj,
        task='habits.tasks.enable_notifications',
        start_time=start_time,
        args=[obj.pk],
        expires=datetime.utcnow() + timedelta(seconds=30)
    )
