"""
Models for Income/Revenue
"""
from uuid import uuid4

from django.db import models
from user.models import User


class Income(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True, db_index=True,
        default=uuid4, editable=False
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name_of_revenue = models.CharField(max_length=255)
    amount = models.PositiveBigIntegerField()

    def __str__(self):
        return self.name_of_revenue


# Create your models here.
