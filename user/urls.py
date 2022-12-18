"""
Urls for User APIs
"""
from django.urls import path

from .views import (
    CreateUserView, LoginUserView, LogoutUserView
)

app_name = "auth"


urlpatterns = [
    path("signup/", CreateUserView.as_view(), name='signup'),
    path("login/", LoginUserView.as_view(), name='login'),
    path("logout/", LogoutUserView.as_view(), name="logout"),
    ]
