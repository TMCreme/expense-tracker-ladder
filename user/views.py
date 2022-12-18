from django.shortcuts import render
from django.contrib.auth import authenticate

from rest_framework import generics, status
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

# from .models import User

from .serializers import (
    AuthTokenSerializer, UserSerializer,
    # JsonAuthTokenSerializer
)


class CreateUserView(generics.CreateAPIView):
    """Signup API"""
    serializer_class = UserSerializer


class LoginUserView(TokenObtainPairView):

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
        else:
            return Response({
                "error": "Invalid Username/Password"
            }, status=status.HTTP_400_BAD_REQUEST)


# Create your views here.
