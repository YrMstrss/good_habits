from django.conf import settings
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')
    place = models.CharField(max_length=100, verbose_name='место')
    time = models.TimeField(verbose_name='время')
    action = models.CharField(max_length=200, verbose_name='действие')
    is_nice = models.BooleanField(default=False, verbose_name='приятная привычка')
    linked_habit = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='связанная привычка', **NULLABLE)
    reward = models.CharField(max_length=200, verbose_name='вознаграждение', **NULLABLE)
    time_to_complete = models.IntegerField(verbose_name='время на выполнение')
    is_public = models.BooleanField(verbose_name='публичная привычка')

    def __str__(self):
        return f'{self.action} в {self.time} в {self.place}'

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
