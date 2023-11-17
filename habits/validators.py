from rest_framework.exceptions import ValidationError

from habits.models import Habit


class HabitTimeToCompleteValidator:

    """Валидатор для проверки времени выполнения привычки"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_value = dict(value).get(self.field)
        if not 0 < tmp_value <= 120:
            raise ValidationError('Время выполнения привычки должно быть больше 0 и меньше 120 секунд')


class LinkedHabitValidator:

    """Валидатор для проверки является ли связанная привычка приятной"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_value = dict(value).get(self.field)
        if tmp_value:
            if not tmp_value.is_nice:
                raise ValidationError('Связанная привычка должна быть приятной')


class RewardAndLinkedHabitValidator:

    """
    Валидатор для проверки, что у привычки не указанны одновременно связанная привычка и вознаграждение, или не указано
    ни вознаграждения, ни связанной привычки
    """

    def __init__(self, field_1, field_2):
        self.field_1 = field_1
        self.field_2 = field_2

    def __call__(self, value):
        tmp_value_1 = dict(value).get(self.field_1)
        tmp_value_2 = dict(value).get(self.field_2)
        if tmp_value_1 and tmp_value_2:
            raise ValidationError('У привычки не может быть одновременно и связанной привычки, и вознаграждения')
        elif not tmp_value_1 and not tmp_value_2:
            raise ValidationError('У полезной привычки должно быть или вознаграждение, или связанная привычка')


class NiceHabitValidator:
    """
    Валидатор для проверки, что у приятной привычки не указано вознаграждение или связанная привычка
    """
    def __init__(self, field_1, field_2, field_3):
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def __call__(self, value):
        tmp_value_1 = dict(value).get(self.field_1)
        tmp_value_2 = dict(value).get(self.field_2)
        tmp_value_3 = dict(value).get(self.field_3)

        if tmp_value_1:
            if tmp_value_2 or tmp_value_3:
                raise ValidationError('У приятной привычки не может быть связанной привычки или вознаграждения')
