from rest_framework.exceptions import ValidationError


class HabitTimeToCompleteValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_value = dict(value).get(self.field)
        if not 0 < tmp_value <= 120:
            raise ValidationError('Время выполнения привычки должно быть больше 0 и меньше 120 секунд')


class LinkedHabitValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_value = dict(value).get(self.field)
        if not tmp_value.is_nice:
            raise ValidationError('Связанная привычка должна быть приятной')
