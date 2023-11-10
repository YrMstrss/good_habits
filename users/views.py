from rest_framework import generics
from rest_framework.permissions import AllowAny

from users.models import User
from users.permissions import IsCurrentUser
from users.serializers import UserRegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsCurrentUser]
