from django.urls import path

from .views import (
    CreateUserView, LoginUserView
)

app_name = "app"


urlpatterns = [
    path('signup/', CreateUserView.as_view(), name='signup'),
    path('login/', LoginUserView.as_view(), name='token'),
    ]
