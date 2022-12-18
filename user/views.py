"""
API Views for the user
"""
# from django.shortcuts import render
from django.contrib.auth import authenticate

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .models import User

from .serializers import (
    AuthTokenSerializer, UserSerializer,
    LogoutSerializer
)


class CreateUserView(generics.CreateAPIView):
    """Signup API"""
    serializer_class = UserSerializer


class UserUpdateGetView(generics.RetrieveUpdateAPIView):
    """get user profile and update"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    # queryset = User.objects.all()
    # lookup_field = "pk"

    def patch(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=self.kwargs["pk"])
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = User.objects.get(pk=self.kwargs["pk"])
        serializer = self.get_serializer(
            instance, data=request.data, partial=True
            )

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User details updated successfully!"})

        else:
            return Response({"message": serializer.errors})


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
            # access_token = token.access_token
            # print(access_token)
            if token:
                token.blacklist()
                # access_token.blacklist()
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
