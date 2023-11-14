import os

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from rest_framework import generics
from rest_framework.permissions import AllowAny

from users.models import User
from users.permissions import IsCurrentUser
from users.serializers import UserRegisterSerializer, UserSerializer
from users.services import get_chat_ids


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


class UserGetChatIdView(View):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)

        token = os.getenv('TG_BOT_API_KEY')
        chat_ids = get_chat_ids(token)
        key = user.telegram_username
        if key in chat_ids.keys():
            chat_id = chat_ids[key]
            user.chat_id = chat_id
            user.save()

        return redirect(reverse_lazy('users:view-user', args=[pk]))
