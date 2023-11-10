from rest_framework import serializers

from habits.models import Habit
from habits.validators import HabitTimeToCompleteValidator


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        validators = [HabitTimeToCompleteValidator(field='time_to_complete')]
