from rest_framework import generics

from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.permisions import IsOwner, IsPublic
from habits.serializers import HabitSerializer
from habits.services import create_periodic_task


class HabitCreateAPIView(generics.CreateAPIView):
    """
    Контроллер для создания новой привычки
    """
    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        """
        Метод для привязки текущего пользователя к созданной привычке и для вызова функции, создающей периодическую
        задачу
        """
        habit = serializer.save()
        habit.user = self.request.user
        habit.save()

        create_periodic_task(habit)


class HabitListAPIView(generics.ListAPIView):
    """
    Контроллер для просмотра списка привычек
    """
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator

    def get_queryset(self):
        """
        Метод, получающий список привычек текущего пользователя и публичные привычки других пользователей
        """
        user = self.request.user

        queryset_owner = Habit.objects.filter(user=user)
        queryset_public = Habit.objects.filter(is_public=True)

        return queryset_owner.union(queryset_public)

    def get(self, request, **kwargs):
        """
        Метод для пагинации выводимого списка привычек
        """
        queryset = self.get_queryset()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = HabitSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """
    Контроллер для просмотра одной привычки
    """
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsOwner | IsPublic]


class HabitUpdateAPIView(generics.UpdateAPIView):
    """
    Контроллер для редактирования пользователем своих привычек
    """
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsOwner]


class HabitDestroyAPIView(generics.DestroyAPIView):
    """
    Контроллер для удаления пользователем своих привычек
    """
    queryset = Habit.objects.all()
    permission_classes = [IsOwner]
