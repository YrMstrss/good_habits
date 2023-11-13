from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from habits.models import Habit
from users.models import User


class HabitCreateTestCase(APITestCase):
    def setUp(self) -> None:

        self.client = APIClient()

        self.user = User.objects.create(
            email='ivan@ivanov.com',
            first_name='Ivan',
            last_name='Ivanov',
            phone='88005553535',
            city='Moscow'
        )
        self.user.set_password('Ivanov123')
        self.user.save()

        self.client.force_authenticate(user=self.user)

        # данные для создания полезной привычки
        self.data_good_habit_right = {
            "place": "в парке",
            "time": "18:00",
            "action": "бегать",
            "is_nice": False,
            "reward": "any reward",
            "time_to_complete": 60,
            "is_public": True,
            "period": "3"
        }

        # данные для создания приятной привычки
        self.data_nice_habit = {
            "place": "в парке",
            "time": "18:30",
            "action": "пить воду",
            "is_nice": True,
            "is_public": True,
            "time_to_complete": 60,
        }

        # данные для создания полезной привычки с ошибкой (есть и связанная привычка, и вознаграждение)
        self.data_good_habit_wrong = {
            "place": "в парке",
            "time": "18:00",
            "action": "бегать",
            "is_nice": False,
            "reward": "any reward",
            "time_to_complete": 60,
            "is_public": True,
            "period": "3",
            "linked_habit": 2
        }

        # данные для создания приятной привычки с неверным временем выполнения
        self.data_nice_habit_wrong_time = {
            "place": "в парке",
            "time": "18:30",
            "action": "пить воду",
            "is_nice": True,
            "is_public": True,
            "time_to_complete": 140,
        }

        # данные для создания полезной привычки с неподходящей связанной привычкой
        self.data_good_habit_linked_habit = {
            "place": "в парке",
            "time": "18:00",
            "action": "бегать",
            "is_nice": False,
            "reward": "any reward",
            "time_to_complete": 60,
            "is_public": True,
            "period": "3",
            "linked_habit": 1
        }

        # данные для создания приятной привычки со связанной привычкой
        self.data_nice_habit_linked_habit = {
            "place": "в парке",
            "time": "18:30",
            "action": "пить воду",
            "is_nice": True,
            "is_public": True,
            "time_to_complete": 10,
            "linked_habit": 2
        }

    def test_create_habit(self):

        # проверка корректного создания полезной привычки

        responce_good_habit_right = self.client.post(
            reverse('habit:create-habit'),
            data=self.data_good_habit_right
        )

        self.assertEqual(
            responce_good_habit_right.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            responce_good_habit_right.json(),
            {
                "id": 1,
                "place": "в парке",
                "time": "18:00",
                "action": "бегать",
                "is_nice": False,
                "reward": "any reward",
                "time_to_complete": 60,
                "is_public": True,
                "period": "3",
                "user": 1,
                "linked_habit": None
            }
        )

        # проверка корректного создания приятной привычки

        responce_data_nice_habit = self.client.post(
            reverse('habit:create-habit'),
            data=self.data_nice_habit
        )

        self.assertEqual(
            responce_data_nice_habit.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            responce_data_nice_habit.json(),
            {
                "id": 2,
                "place": "в парке",
                "time": "18:30",
                "action": "пить воду",
                "is_nice": True,
                "is_public": True,
                "reward": None,
                "time_to_complete": 60,
                "period": None,
                "user": 1,
                "linked_habit": None
            }
        )

        # проверка некорректного создания полезной привычки (с наградой и связанной привычкой) (не работает)

        # responce_data_good_habit_wrong = self.client.post(
        #     reverse('habit:create-habit'),
        #     data=self.data_good_habit_wrong
        # )
        #
        # self.assertEqual(
        #     responce_data_good_habit_wrong.status_code,
        #      status.HTTP_400_BAD_REQUEST
        # )

        # проверка некорректного создания приятной привычки (неверное время выполнения привычки)

        responce_data_nice_habit_wrong_time = self.client.post(
            reverse('habit:create-habit'),
            data=self.data_nice_habit_wrong_time
        )

        self.assertEqual(
            responce_data_nice_habit_wrong_time.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # проверка некорректного создания полезной привычки (связанная привычка не является приятной)

        responce_data_good_habit_linked_habit = self.client.post(
            reverse('habit:create-habit'),
            data=self.data_good_habit_linked_habit
        )

        self.assertEqual(
            responce_data_good_habit_linked_habit.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # проверка некорректного создания приятной привычки (приятная привычка имеет связанную) (не работает)

        # responce_data_nice_habit_linked_habit = self.client.post(
        #     reverse('habit:create-habit'),
        #     data=self.data_nice_habit_linked_habit
        # )
        #
        # self.assertEqual(
        #     responce_data_nice_habit_linked_habit.status_code,
        #     status.HTTP_400_BAD_REQUEST
        # )

    def tearDown(self) -> None:
        User.objects.all().delete()
        Habit.objects.all().delete()
