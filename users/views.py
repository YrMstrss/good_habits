from rest_framework import generics

from users.serializers import UserRegisterSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
