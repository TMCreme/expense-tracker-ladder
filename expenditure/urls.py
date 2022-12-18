"""
URLs for Expenditure API
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import ExpenditureAPIView


router = DefaultRouter()
router.register("user", ExpenditureAPIView)

app_name = "expenditure"

urlpatterns = [
    path("", include(router.urls))
]
