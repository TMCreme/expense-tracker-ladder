"""
Serializers for Expenditure
"""
from rest_framework import serializers
from .models import Expenditure


class ExpenditureSerializer(serializers.ModelSerializer):
    """Serializer for Expenditure Model"""

    class Meta:
        model = Expenditure
        fields = [
            "id", "category", "name_of_item", "estimated_amount"
        ]
        read_only_fields = ["id"]
