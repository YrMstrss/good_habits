from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        cls.user_1 = User.objects.create(
            id=1,
            email='ivan@ivanov.com',
            first_name='Ivan',
            last_name='Ivanov',
            phone='88005553535',
            city='Moscow'
        )

        cls.user_2 = User.objects.create(
            id=2,
            email='petr@petrov.com',
            first_name='Petr',
            last_name='Petrov',
            phone='88009007001',
            city='Moscow'
        )

        cls.nice_habit = Habit.objects.create(
            place="в парке",
            time="18:30",
            action="пить воду",
            is_nice=True,
            is_public=False,
            time_to_complete=60,
            user_id=1

        )

        cls.good_habit = Habit.objects.create(
            place="в парке",
            time="18:00",
            action="бегать",
            is_nice=False,
            reward="any reward",
            time_to_complete=60,
            is_public=False,
            period="3",
            user_id=1
        )

        # данные для создания полезной привычки
        cls.data_good_habit_right = {
            "place": "в парке",
            "time": "18:00",
            "action": "бегать",
            "is_nice": False,
            "reward": "any reward",
            "time_to_complete": 60,
            "is_public": False,
            "period": "3"
        }

        # данные для создания приятной привычки
        cls.data_nice_habit = {
            "place": "в парке",
            "time": "18:30",
            "action": "пить воду",
            "is_nice": True,
            "is_public": False,
            "time_to_complete": 60,
        }

        # данные для создания полезной привычки с ошибкой (есть и связанная привычка, и вознаграждение)
        cls.data_good_habit_wrong = {
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
        cls.data_nice_habit_wrong_time = {
            "place": "в парке",
            "time": "18:30",
            "action": "пить воду",
            "is_nice": True,
            "is_public": True,
            "time_to_complete": 140,
        }

        # данные для создания полезной привычки с неподходящей связанной привычкой
        cls.data_good_habit_linked_habit = {
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
        cls.data_nice_habit_linked_habit = {
            "place": "в парке",
            "time": "18:30",
            "action": "пить воду",
            "is_nice": True,
            "is_public": True,
            "time_to_complete": 10,
            "linked_habit": 2
        }

        # данные для обновления привычки
        cls.data_for_update = {
            "place": "на стадионе",
            "time": "18:00",
            "action": "бегать",
            "is_nice": False,
            "reward": "any reward",
            "time_to_complete": 40,
            "is_public": True,
            "period": "3"
        }

    def test_create_habit_right(self):
        """
        Тест на создание привычки
        """
        self.client.force_authenticate(user=self.user_1)

        response = self.client.post(
            reverse('habit:create-habit'),
            data=self.data_good_habit_right
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {
                "id": 3,
                "place": "в парке",
                "time": "18:00",
                "action": "бегать",
                "is_nice": False,
                "reward": "any reward",
                "time_to_complete": 60,
                "is_public": False,
                "period": "3",
                "user": 1,
                "linked_habit": None
            }
        )

        response = self.client.post(
            reverse('habit:create-habit'),
            data=self.data_nice_habit
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {
                "id": 4,
                "place": "в парке",
                "time": "18:30",
                "action": "пить воду",
                "is_nice": True,
                "is_public": False,
                "reward": None,
                "time_to_complete": 60,
                "period": None,
                "user": 1,
                "linked_habit": None
            }
        )

    def test_create_good_habit_wrong(self):
        """
        Тест на создание полезной привычки с неверными данными (указаны и связанная привычка и вознаграждение)
        """
        self.client.force_authenticate(user=self.user_1)

        response = self.client.post(
            reverse('habit:create-habit'),
            data=self.data_good_habit_wrong
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_create_habit_wrong_time(self):
        """
        Тест на создание привычки с неверным временем выполнения
        """
        self.client.force_authenticate(user=self.user_1)

        response = self.client.post(
            reverse('habit:create-habit'),
            data=self.data_nice_habit_wrong_time
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_create_habit_with_wrong_linked(self):
        """
        Тест на создание привычки с указанием в качестве связанной привычки - полезной привычки
        """
        self.client.force_authenticate(user=self.user_1)

        response = self.client.post(
            reverse('habit:create-habit'),
            data=self.data_good_habit_linked_habit
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_create_nice_habit_with_linked(self):
        """
        Тест на создание приятной привычки имеющей связанную
        """
        self.client.force_authenticate(user=self.user_1)

        response = self.client.post(
            reverse('habit:create-habit'),
            data=self.data_nice_habit_linked_habit
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_read_habit_list(self):
        """
        Тест на чтение списка привычек
        """
        self.client.force_authenticate(user=self.user_1)

        response = self.client.get(
            reverse('habit:list-habit')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {"count": 2,
             "next": None,
             "previous": None,
             "results": [
                 {
                     "id": 2,
                     "place": "в парке",
                     "time": "18:00",
                     "action": "бегать",
                     "is_nice": False,
                     "reward": "any reward",
                     "time_to_complete": 60,
                     "is_public": False,
                     "period": "3",
                     "user": self.user_1.id,
                     "linked_habit": None

                 },
                 {
                     "id": 1,
                     "place": "в парке",
                     "time": "18:30",
                     "action": "пить воду",
                     "is_nice": True,
                     "is_public": False,
                     "reward": None,
                     "time_to_complete": 60,
                     "period": None,
                     "user": 1,
                     "linked_habit": None
                 },
             ]
             }
        )

        self.client.force_authenticate(user=self.user_2)

        response = self.client.get(
            reverse('habit:list-habit')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {"count": 0,
             "next": None,
             "previous": None,
             "results": [

             ]
             }
        )

    def test_read_single_habit_by_owner(self):
        """
        Тест на чтение одной привычки владельцем привычки
        """
        self.client.force_authenticate(user=self.user_1)

        response = self.client.get(
            reverse('habit:view-habit', args=[1])
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "id": 1,
                "place": "в парке",
                "time": "18:30",
                "action": "пить воду",
                "is_nice": True,
                "is_public": False,
                "reward": None,
                "time_to_complete": 60,
                "period": None,
                "user": 1,
                "linked_habit": None
            }
        )

    def test_read_single_habit_by_other_user(self):
        """
        Тест на чтение приватной привычки пользователем, не являющимся владельцем
        """
        self.client.force_authenticate(user=self.user_2)

        response = self.client.get(
            reverse('habit:view-habit', args=[1])
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_update_habit_by_owner(self):
        """
        Тест на редактирование привычки владельцем
        """
        self.client.force_authenticate(user=self.user_1)

        response = self.client.put(
            reverse('habit:update-habit', args=[2]),
            self.data_for_update
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "id": 2,
                "place": "на стадионе",
                "time": "18:00",
                "action": "бегать",
                "is_nice": False,
                "reward": "any reward",
                "time_to_complete": 40,
                "is_public": True,
                "period": "3",
                "linked_habit": None,
                "user": 1
            }
        )

    def test_update_habit_by_other_user(self):
        """
        Тест на редактирование привычки пользователем, не являющимся владельцем
        """
        self.client.force_authenticate(user=self.user_2)

        response = self.client.put(
            reverse('habit:update-habit', args=[2]),
            self.data_for_update
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_delete_habit_by_other_user(self):
        """
        Тест на удаление привычки пользователем, не являющимся владельцем
        """
        self.client.force_authenticate(user=self.user_2)

        response = self.client.delete(
            reverse('habit:delete-habit', args=[1])
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_delete_habit_by_owner(self):
        """
        Тест на удаление привычки владельцем
        """
        self.client.force_authenticate(user=self.user_1)

        response = self.client.delete(
            reverse('habit:delete-habit', args=[1])
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
