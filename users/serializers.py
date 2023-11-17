from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from users.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для регистрации пользователя
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('email', 'password')


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели пользователя
    """

    class Meta:
        model = User
        exclude = ('password', )
        read_only_fields = ['chat_id', ]
