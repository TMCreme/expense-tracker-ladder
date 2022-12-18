"""
Urls for User APIs
"""
from django.urls import path

from .views import (
    CreateUserView, LoginUserView, LogoutUserView,
    UserUpdateGetView
)

app_name = "auth"


urlpatterns = [
    path("signup/", CreateUserView.as_view(), name='signup'),
    path("login/", LoginUserView.as_view(), name='login'),
    path("logout/", LogoutUserView.as_view(), name="logout"),
    path(
        "user/<uuid:pk>/profile/",
        UserUpdateGetView.as_view(),
        name="user-profile"
        ),
    ]
