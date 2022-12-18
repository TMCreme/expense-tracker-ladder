"""
Views for Income API
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Income

from .serializers import IncomeSerializer


class IncomeAPIView(viewsets.ModelViewSet):
    """Create and List User's income data"""
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]
    queryset = Income.objects.all()

    def get_queryset(self):
        """Retrieve user's income data"""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Create your views here.
