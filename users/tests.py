from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class UserTestCase(APITestCase):
    """Тест-кейс модели пользователя """
    def setUp(self) -> None:
        self.client = APIClient()

        self.data = {
            'email': 'ivan@gmail.com',
            'password': 'Ivanov123'
        }

    def test_register_user(self):

        """Тест регистрации пользователя"""

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
