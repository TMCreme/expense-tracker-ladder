"""
API Views for the user
"""
# from django.shortcuts import render
from django.contrib.auth import authenticate

from rest_framework import generics, status
from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

# from .models import User

from .serializers import (
    AuthTokenSerializer, UserSerializer,
    LogoutSerializer
)


class CreateUserView(generics.CreateAPIView):
    """Signup API"""
    serializer_class = UserSerializer


class LoginUserView(TokenObtainPairView):
    """Custom API View for Access and Refresh token"""

    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(
                email=email,
                password=password,
            )
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "id": user.id,
                "email": email,
                "tokens": {
                    "refresh_token": str(refresh),
                    "access_token": str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)
        return Response({
            "error": "Invalid Username/Password"
        }, status=status.HTTP_400_BAD_REQUEST)


class LogoutUserView(APIView):
    """Logout View for user tokens"""
    # permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            if token:
                token.blacklist()
                return Response({
                    "message": "User logged out successfully"
                })
            return Response({
                "error": "Invalid refresh token"
            }, status=status.HTTP_400_BAD_REQUEST)
        except TokenError as tke:
            print(tke)
            return Response({
                "error": "Invalid refresh token"
            }, status=status.HTTP_400_BAD_REQUEST)


# Create your views here.
