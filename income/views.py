"""
Views for Income API
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Income

from .serializers import IncomeSerializer


class IncomeAPIView(viewsets.ModelViewSet):
    """Operations about a user's income"""
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]
    queryset = Income.objects.all()

    def get_queryset(self):
        """Override queryset to filter for user"""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Create your views here.
