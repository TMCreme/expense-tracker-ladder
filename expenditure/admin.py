"""
Register Model for Admin
"""
from django.contrib import admin

from .models import Expenditure


admin.site.register(Expenditure)

# Register your models here.
