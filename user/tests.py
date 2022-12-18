"""
Test cases for User APIs
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


SIGNUP_URL = reverse("auth:signup")
LOGIN_URL = reverse("auth:login")


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


# Create your tests here.
