"""
Views for the user's Expenditure
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Expenditure

from .serializers import ExpenditureSerializer


class ExpenditureAPIView(viewsets.ModelViewSet):
    """Operations about a user's expenditure"""
    serializer_class = ExpenditureSerializer
    permission_classes = [IsAuthenticated]
    queryset = Expenditure.objects.all()

    def get_queryset(self):
        """Override queryset to filter for user"""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Create your views here.
