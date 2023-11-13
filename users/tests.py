from datetime import timedelta

from django.urls import reverse
from django.utils.timezone import now
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from users.models import User


class UserRegisterTestCase(APITestCase):
    """Тест-кейс модели пользователя """
    def setUp(self) -> None:
        self.client = APIClient()

        self.data = {
            'email': 'ivan@gmail.com',
            'password': 'Ivanov123'
        }


class UserTestCase(APITestCase):
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

    def test_profile_view(self):

        """Тест просмотра профиля пользователя"""

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
                "id": 1,
                "last_login": None,
                "is_superuser": False,
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
