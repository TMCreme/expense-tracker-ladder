"""
Models for Expenditure
"""
from uuid import uuid4

from django.db import models
from user.models import User


class Expenditure(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True, db_index=True,
        default=uuid4, editable=False
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=255)
    name_of_item = models.CharField(max_length=255)
    estimated_amount = models.PositiveBigIntegerField()

    def __str__(self) -> str:
        return self.name_of_item


# Create your models here.
