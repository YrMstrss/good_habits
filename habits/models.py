from django.conf import settings
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Habit(models.Model):
    PERIOD_CHOICES = (
        ('1', 'Раз в день'),
        ('2', 'Раз в два дня'),
        ('3', 'Раз в три дня'),
        ('4', 'Раз в четыре дня'),
        ('5', 'Раз в пять дней'),
        ('6', 'Раз в шесть дней'),
        ('7', 'Раз в неделю'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь',
                             **NULLABLE)
    place = models.CharField(max_length=100, verbose_name='место', **NULLABLE)
    time = models.TimeField(verbose_name='время', **NULLABLE)
    action = models.CharField(max_length=200, verbose_name='действие')
    is_nice = models.BooleanField(default=False, verbose_name='приятная привычка')
    linked_habit = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='связанная привычка', **NULLABLE)
    reward = models.CharField(max_length=200, verbose_name='вознаграждение', **NULLABLE)
    time_to_complete = models.IntegerField(verbose_name='время на выполнение')
    is_public = models.BooleanField(verbose_name='публичная привычка')
    period = models.CharField(max_length=1, choices=PERIOD_CHOICES, verbose_name='периодичность',
                              **NULLABLE)

    def __str__(self):
        return f'{self.action} в {self.time} в {self.place}'

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
