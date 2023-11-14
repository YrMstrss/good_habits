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


def reward_and_linked_habit_validator(obj: Habit) -> None:

    """
    Валидатор для проверки, что у привычки не указанны одновременно связанная привычка и вознаграждение, или не указано
    ни вознаграждения, ни связанной привычки
    :param obj: Объект типа Habit
    :return: None
    """

    if obj.linked_habit and obj.reward:
        raise ValidationError('У привычки не может быть одновременно и связанной привычки, и вознаграждения')
    elif not obj.linked_habit and not obj.reward:
        raise ValidationError('У полезной привычки должно быть или вознаграждение, или связанная привычка')


def nice_habit_validator(obj: Habit):

    """
    Валидатор для проверки, что у приятной привычки не указано вознаграждение или связанная привычка
    :param obj: Объект типа Habit
    :return: None
    """

    if obj.is_nice:
        if obj.linked_habit or obj.reward:
            raise ValidationError('У приятной привычки не может быть связанной привычки или вознаграждения')
