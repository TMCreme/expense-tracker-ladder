"""
Test cases for User APIs
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from user.models import User


SIGNUP_URL = reverse("auth:signup")
LOGIN_URL = reverse("auth:login")
LOGOUT_URL = reverse("auth:logout")


def create_user(**params):
    """Signup and return a new user"""
    return get_user_model().objects.create_user(**params)


class UserAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_user_signup_success(self):
        """Test a successful signup"""
        payload = {
            "email": "test@example.com",
            "password": "testpasswd123",
            "first_name": "Test",
            "last_name": "Test",
            "username": "testuser"
        }

        response = self.client.post(SIGNUP_URL, payload)

        # Test successful sign up
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Test Password is not returned in response data
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)

    def test_user_with_email_exists_error(self):
        """Try signup with an already existing email"""
        payload = {
            "email": "test@example.com",
            "password": "testpasswd123",
            "first_name": "Test",
            "last_name": "Test",
            "username": "testuser"
        }
        create_user(**payload)

        response = self.client.post(SIGNUP_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_too_short_password(self):
        """Test signup with a shorter password"""
        payload = {
            "email": "test@example.com",
            "password": "12",
            "first_name": "Test",
            "last_name": "Test",
            "username": "testuser"
        }
        response = self.client.post(SIGNUP_URL, payload)
        # Test password too short
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Confirm user was not created
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_login_for_token(self):
        """Test login to obtain token"""
        payload = {
            "email": "test@example.com",
            "password": "testpasswd123",
            "first_name": "Test",
            "last_name": "Test",
            "username": "testuser"
        }
        create_user(**payload)

        response = self.client.post(
            LOGIN_URL,
            {
                "email": "test@example.com",
                "password": "testpasswd123"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("tokens", response.data)
        self.assertIn("email", response.data)
        self.assertIn("id", response.data)

    def test_wrong_credentials(self):
        """Login to obtain token with wrong password"""
        payload = {
            "email": "test@example.com",
            "password": "testpasswd123"
        }
        create_user(**payload)

        response = self.client.post(
            LOGIN_URL,
            {
                "email": "test@example.com",
                "password": "password"
            }
            )

        self.assertNotIn("tokens", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_with_empty_password(self):
        """Signup with empty string for password"""
        payload = {
            "email": "test@example.com",
            "password": ""
        }

        response = self.client.post(SIGNUP_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertNotIn("")

    def test_login_without_creating_user(self):
        """Login with user that does not exist"""
        payload = {
            "email": "test@example.com",
            "password": "testpasswd123"
        }

        response = self.client.post(LOGIN_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_successful_logout(self):
        """Test successful logout"""
        payload = {
            "email": "test@example.com",
            "password": "testpasswd123",
            "first_name": "Test",
            "last_name": "Test",
            "username": "testuser"
        }
        create_user(**payload)

        login_user = self.client.post(
            LOGIN_URL,
            {
                "email": "test@example.com",
                "password": "testpasswd123"
            }
        )

        response = self.client.post(
            LOGOUT_URL,
            {
                "refresh": login_user.data["tokens"]["refresh_token"]
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_with_no_refresh_token(self):
        """Test logout without refresh token"""
        response = self.client.post(
            LOGOUT_URL,
            {
                "refresh": ""
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_with_access_token_value_with_refresh_key(self):
        """Refresh key will have access token"""
        payload = {
            "email": "test@example.com",
            "password": "testpasswd123",
            "first_name": "Test",
            "last_name": "Test",
            "username": "testuser"
        }
        create_user(**payload)

        login_user = self.client.post(
            LOGIN_URL,
            {
                "email": "test@example.com",
                "password": "testpasswd123"
            }
        )

        response = self.client.post(
            LOGOUT_URL,
            {
                "refresh": login_user.data["tokens"]["access_token"]
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_profile_success(self):
        """Test getting profile successfully"""

        payload = {
            "email": "test@example.com",
            "password": "testpasswd123"
        }

        create_user(**payload)
        user = User.objects.get(email=payload['email'])

        client = APIClient()
        client.force_authenticate(user)
        GET_UPDATE_URL = reverse("auth:user-profile", args=[user.id])

        response = client.get(
            GET_UPDATE_URL
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("email", response.data)
        self.assertNotIn("password", response.data)
        self.assertIn("id", response.data)

    def test_get_profile_without_auth(self):
        """Testing profile get without Auth"""
        payload = {
            "email": "test@example.com",
            "password": "testpasswd123"
        }

        create_user(**payload)
        user = User.objects.get(email=payload['email'])

        GET_UPDATE_URL = reverse("auth:user-profile", args=[user.id])

        response = self.client.get(
            GET_UPDATE_URL
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_profile_success(self):
        """Testing update on Profile with successfully"""
        payload = {
            "email": "test@example.com",
            "password": "testpasswd123"
        }

        create_user(**payload)
        user = User.objects.get(email=payload['email'])

        client = APIClient()
        client.force_authenticate(user)
        GET_UPDATE_URL = reverse("auth:user-profile", args=[user.id])

        response = client.put(
            GET_UPDATE_URL,
            {"first_name": "tester", "last_name": "testuser"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_profile_with_patch(self):
        """Testing patch restriction"""
        payload = {
            "email": "test@example.com",
            "password": "testpasswd123"
        }

        create_user(**payload)
        user = User.objects.get(email=payload['email'])

        client = APIClient()
        client.force_authenticate(user)
        GET_UPDATE_URL = reverse("auth:user-profile", args=[user.id])

        response = client.patch(
            GET_UPDATE_URL,
            {"first_name": "tester", "last_name": "testuser"}
        )

        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
            )


# Create your tests here.
