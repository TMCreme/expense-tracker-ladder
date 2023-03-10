"""
Serializers for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
)

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        """Meta data for User serializer"""
        model = get_user_model()
        fields = [
            'id', 'email', 'password',
            'first_name', 'last_name', 'username'
            ]
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5},
            'id': {'read_only': True}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )


class LogoutSerializer(serializers.Serializer):
    """Serializer class for logout allow for a field"""
    refresh = serializers.CharField()
