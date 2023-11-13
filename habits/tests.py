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

        self.data_good_right = {
            "place": "в парке",
            "time": "18:00",
            "action": "бегать",
            "is_nice": False,
            "reward": "any reward",
            "time_to_complete": 60,
            "is_public": True,
            "period": "3"
        }

    def test_create_good_habit(self):

        responce = self.client.post(
            reverse('habit:create-habit'),
            data=self.data_good_right
        )

        self.assertEqual(
            responce.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            responce.json(),
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

    def tearDown(self) -> None:
        User.objects.all().delete()
        Habit.objects.all().delete()
