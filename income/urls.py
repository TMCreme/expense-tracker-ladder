"""
Urls for Income API
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import IncomeAPIView


router = DefaultRouter()
router.register("user", IncomeAPIView, basename="user-income")

app_name = "income"

urlpatterns = [
    path('', include(router.urls))
]
