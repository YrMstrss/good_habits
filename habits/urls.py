from django.urls import path

from habits.apps import HabitsConfig
from habits.views import HabitCreateAPIView, HabitListAPIView, HabitRetrieveAPIView, HabitUpdateAPIView, \
    HabitDestroyAPIView

app_name = HabitsConfig.name

urlpatterns = [
    path('create/', HabitCreateAPIView.as_view(), name='create-habit'),
    path('list/', HabitListAPIView.as_view(), name='list-habit'),
    path('<int:pk>', HabitRetrieveAPIView.as_view(), name='view-habit'),
    path('update/<int:pk>', HabitUpdateAPIView.as_view(), name='update-habit'),
    path('delete/<int:pk>', HabitDestroyAPIView.as_view(), name='delete-habit'),
]
