from django.urls import path

from users.views import (
    IdentityAPIView,
    LoginAPIView,
    LogoutAPIView,
    RegisterAPIView,
    UserListAPIView,
    refresh_token_api_view,
)

urlpatterns = [
    path("users/", UserListAPIView.as_view(), name="users"),
    path("auth/register/", RegisterAPIView.as_view(), name="register"),
    path("auth/refresh-token/", refresh_token_api_view, name="refresh-token"),
    path("auth/login/", LoginAPIView.as_view(), name="login"),
    path("auth/logout/", LogoutAPIView.as_view(), name="logout"),
    path("identity/", IdentityAPIView.as_view(), name="identity"),
]
