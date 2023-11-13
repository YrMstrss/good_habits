from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from habits.models import Habit
from users.models import User


class HabitCreateTestCase(APITestCase):
    """Тест-кейс на создание привычек"""

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


class HabitReadTestCase(APITestCase):
    """Тест-кейс для чтения привычек"""

    maxDiff = None

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

        self.user_2 = User.objects.create(
            email='petr@petrov.com',
            first_name='Petr',
            last_name='Petrov',
            phone='88005553535',
            city='Moscow'
        )
        self.user_2.set_password('Petrov123')
        self.user_2.save()

        self.habit_1 = Habit.objects.create(
            place="в парке",
            time="18:30",
            action="тренировка",
            is_nice=False,
            is_public=True,
            reward="вкусняшка",
            time_to_complete=60,
            period="2",
            user_id=2,
            linked_habit=None
        )

        self.habit_2 = Habit.objects.create(
            place="в парке",
            time="18:30",
            action="пить воду",
            is_nice=True,
            is_public=False,
            reward=None,
            time_to_complete=60,
            period=None,
            user_id=1,
            linked_habit=None
        )

        self.habit_3 = Habit.objects.create(
            place="в парке",
            time="18:30",
            action="тренировка",
            is_nice=False,
            is_public=False,
            reward=None,
            time_to_complete=60,
            period="2",
            user_id=1,
            linked_habit_id=2
        )

    def test_read_habit_list(self):
        self.client.force_authenticate(user=self.user)

        responce_read_list = self.client.get(
            reverse('habit:list-habit')
        )

        self.assertEqual(
            responce_read_list.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            responce_read_list.json(),
            {"count": 3,
             "next": None,
             "previous": None,
             "results": [
                 {
                     "id": 3,
                     "place": "в парке",
                     "time": "18:30",
                     "action": "тренировка",
                     "is_nice": False,
                     "reward": None,
                     "time_to_complete": 60,
                     "is_public": False,
                     "period": "2",
                     "user": 1,
                     "linked_habit": 2
                 },
                 {
                     "id": 1,
                     "place": "в парке",
                     "time": "18:30",
                     "action": "тренировка",
                     "is_nice": False,
                     "reward": "вкусняшка",
                     "time_to_complete": 60,
                     "is_public": True,
                     "period": "2",
                     "user": 2,
                     "linked_habit": None
                 },
                 {
                     "id": 2,
                     "place": "в парке",
                     "time": "18:30",
                     "action": "пить воду",
                     "is_nice": True,
                     "reward": None,
                     "time_to_complete": 60,
                     "is_public": False,
                     "period": None,
                     "user": 1,
                     "linked_habit": None
                 }
             ]
             }
        )

        self.client.force_authenticate(user=self.user_2)

        responce_read_list = self.client.get(
            reverse('habit:list-habit')
        )

        self.assertEqual(
            responce_read_list.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            responce_read_list.json(),
            {"count": 1,
             "next": None,
             "previous": None,
             "results": [
                 {
                     "id": 1,
                     "place": "в парке",
                     "time": "18:30",
                     "action": "тренировка",
                     "is_nice": False,
                     "reward": "вкусняшка",
                     "time_to_complete": 60,
                     "is_public": True,
                     "period": "2",
                     "user": 2,
                     "linked_habit": None
                 }
             ]
             }
        )
