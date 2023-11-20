from datetime import timedelta

from django.urls import reverse
from django.utils.timezone import now
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from users.models import User


class UserRegisterTestCase(APITestCase):
    """Тест-кейс для регистрации пользователя """

    def setUp(self) -> None:
        self.client = APIClient()

        self.data = {
            'email': 'ivan@gmail.com',
            'password': 'Ivanov123'
        }

    def test_register(self):
        response = self.client.post(
            reverse('users:register'),
            data=self.data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {
                'email': 'ivan@gmail.com'
            }
        )


class UserTestCase(APITestCase):

    """
    Тест-кейс для модели пользователя
    """

    @classmethod
    def setUpTestData(cls) -> None:
        cls.client = APIClient()

        cls.user = User.objects.create(
            email='ivan@ivanov.com',
            first_name='Ivan',
            last_name='Ivanov',
            phone='88005553535',
            city='Moscow'
        )

        cls.data = {
            "id": 1,
            "is_superuser": False,
            "first_name": "Ivan",
            "last_name": "Ivanov",
            "is_staff": False,
            "is_active": True,
            "phone": "88005553535",
            "city": "St.Petersburg",
            "email": "ivan@ivanov.com"
        }

    def test_profile_view(self):
        """
        Тест просмотра профиля пользователя
        """

        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            reverse('users:view-user', args=[self.user.id])
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "id": self.user.id,
                "last_login": None,
                "is_superuser": False,
                "chat_id": None,
                "telegram_username": None,
                "first_name": "Ivan",
                "last_name": "Ivanov",
                "is_staff": False,
                "is_active": True,
                "date_joined": (now() + timedelta(hours=3)).strftime("%d.%m.%Y %H:%M"),
                "phone": "88005553535",
                "city": "Moscow",
                "avatar": None,
                "email": "ivan@ivanov.com",
                "groups": [],
                "user_permissions": []
            }
        )

    def test_update_user(self):
        """
        Тест для редактирования профиля пользователя
        """

        self.client.force_authenticate(user=self.user)

        response = self.client.put(
            reverse('users:edit-user', args=[self.user.id]),
            data=self.data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "id": self.user.id,
                "last_login": None,
                "is_superuser": False,
                "chat_id": None,
                "telegram_username": None,
                "first_name": "Ivan",
                "last_name": "Ivanov",
                "is_staff": False,
                "is_active": True,
                "date_joined": (now() + timedelta(hours=3)).strftime("%d.%m.%Y %H:%M"),
                "phone": "88005553535",
                "city": "St.Petersburg",
                "avatar": None,
                "email": "ivan@ivanov.com",
                "groups": [],
                "user_permissions": []
            }
        )
