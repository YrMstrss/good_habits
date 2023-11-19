from rest_framework import serializers

from habits.models import Habit
from habits.validators import HabitTimeToCompleteValidator, LinkedHabitValidator, RewardAndLinkedHabitValidator, \
    NiceHabitValidator, PeriodValidator


class HabitSerializer(serializers.ModelSerializer):
    """Сериалайзер привычки"""
    class Meta:
        model = Habit
        fields = '__all__'
        validators = [
            HabitTimeToCompleteValidator(field='time_to_complete'),
            LinkedHabitValidator(field='linked_habit'),
            RewardAndLinkedHabitValidator(field_1='reward', field_2='linked_habit', field_3='is_nice'),
            NiceHabitValidator(field_1='is_nice', field_2='reward', field_3='linked_habit'),
            PeriodValidator(field_1='is_nice', field_2='period'),
        ]
