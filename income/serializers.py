"""
Serializers for Income
"""
from rest_framework import serializers
from .models import Income


class IncomeSerializer(serializers.ModelSerializer):
    """Searializer for Income model"""

    class Meta:
        model = Income
        fields = ["id", "name_of_revenue", "amount"]
        read_only_fields = ["id"]
