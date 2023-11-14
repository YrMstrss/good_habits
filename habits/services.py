import json
from datetime import datetime, timedelta

from django_celery_beat.models import PeriodicTask, \
    IntervalSchedule

from habits.models import Habit


def create_periodic_task(obj: Habit):
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=int(obj.period),
        period=IntervalSchedule.DAYS,
    )

    if datetime.now().time() < Habit.time:
        start_time = datetime.combine(datetime.today(), Habit.time)
    else:
        start_time = datetime.combine(datetime.today() + timedelta(days=1), Habit.time)

    PeriodicTask.objects.create(
        interval=schedule,
        name=obj,
        task='habits.tasks.enable_notifications',
        start_time=start_time,
        args=json.dumps([obj]),
        kwargs=json.dumps({
            'be_careful': True,
        }),
        expires=datetime.utcnow() + timedelta(seconds=30)
    )
