from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import RegisterView, UserRetrieveAPIView, UserUpdateAPIView, UserGetChatIdView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('<int:pk>', UserRetrieveAPIView.as_view(), name='view-user'),
    path('edit/<int:pk>', UserUpdateAPIView.as_view(), name='edit-user'),
    path('get_chat_id/<int:pk>', UserGetChatIdView.as_view(), name='get-chat-id'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
