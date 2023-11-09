from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import UserManager


class User(AbstractUser):
    phone = models.CharField(max_length=30, verbose_name='номер телефона')
    city = models.CharField(max_length=50, verbose_name='город')
    avatar = models.ImageField(upload_to='user_avatar/', verbose_name='фото', null=True, blank=True)

    email = models.EmailField(unique=True, verbose_name='почта')
    username = None

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
