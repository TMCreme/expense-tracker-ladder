"""
Test cases for the Users Income Endpoints
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

# from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


def create_user(**params):
    """Signup and return a new user"""
    return get_user_model().objects.create_user(**params)


class IncomeAPITests(TestCase):
    """User Income Tests"""

    def setUp(self) -> None:
        self.client = APIClient()
        payload = {
            "email": "test@example.com",
            "password": "testpasswd123",
        }
        user = create_user(**payload)
        self.client.force_authenticate(user)

    def test_add_income_success(self):
        """Test post income by user"""
        payload = {"name_of_revenue": "salary", "amount": 100}
        response = self.client.post("/income/user/", payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertIn("name_of_revenue", response.data)
        self.assertIn("amount", response.data)

    def test_add_income_with_empty_name(self):
        """Test adding income with empty string as name"""
        payload = {"name_of_revenue": "", "amount": 100}
        response = self.client.post("/income/user/", payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_income_with_no_name(self):
        """Add income without the name parameter"""
        payload = {"amount": 100}
        response = self.client.post("/income/user/", payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_with_empty_amount(self):
        """Add income with empty string"""
        payload = {"name_of_revenue": "salary", "amount": ""}
        response = self.client.post("/income/user/", payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_income(self):
        """Add income with negative amount"""
        payload = {"name_of_revenue": "salary", "amount": 100}
        self.client.post("/income/user/", payload)
        response = self.client.get("/income/user/")
        data_size = len(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data_size, 1)

    def test_get_user_income_with_no_data(self):
        """Retrieve user's Income where no income data exists"""
        # Create a record for a different user
        client2 = APIClient()
        user2_payload = {
            "email": "test2@example.com",
            "password": "testpas123",
        }
        user = create_user(**user2_payload)
        client2.force_authenticate(user)
        payload = {"name_of_revenue": "salary", "amount": 100}
        client2.post("/income/user/", payload)

        response = self.client.get("/income/user/")
        data_size = len(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data_size, 0)

    def test_get_an_income_item_by_id(self):
        """Retrieve individual income item by id"""
        payload = {"name_of_revenue": "salary", "amount": 100}
        created_income = self.client.post("/income/user/", payload)
        response = self.client.get("/income/user/{}/".format(
            created_income.data["id"])
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data)
        self.assertIn("name_of_revenue", response.data)
        self.assertIn("amount", response.data)
        self.assertEqual(response.data, created_income.data)

    def test_update_existing_income_data(self):
        """Update an already created income data"""
        payload = {"name_of_revenue": "salary", "amount": 100}
        created_income = self.client.post("/income/user/", payload)
        response = self.client.put(
            "/income/user/{}/".format(created_income.data["id"]),
            {"name_of_revenue": "salary", "amount": 200},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["name_of_revenue"],
            created_income.data["name_of_revenue"]
        )
        self.assertEqual(response.data["amount"], 200)

    def test_update_put_with_partial_data(self):
        """Put Update an already created income data with partial"""
        payload = {"name_of_revenue": "salary", "amount": 100}
        created_income = self.client.post("/income/user/", payload)
        response = self.client.put(
            "/income/user/{}/".format(
                created_income.data["id"]), {"amount": 200}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_existing_income_data_partial(self):
        """Partial Update an already created income data"""
        payload = {"name_of_revenue": "salary", "amount": 100}
        created_income = self.client.post("/income/user/", payload)
        response = self.client.patch(
            "/income/user/{}/".format(
                created_income.data["id"]), {"amount": 200}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["name_of_revenue"],
            created_income.data["name_of_revenue"]
        )
        self.assertEqual(response.data["amount"], 200)

    def test_delete_income_data(self):
        """Delete an existing data"""
        payload = {"name_of_revenue": "salary", "amount": 100}
        created_income = self.client.post("/income/user/", payload)
        response = self.client.delete(
            "/income/user/{}/".format(created_income.data["id"])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_an_already_deleted_item(self):
        """Test multiple delete on an item"""
        payload = {"name_of_revenue": "salary", "amount": 100}
        created_income = self.client.post("/income/user/", payload)
        response = self.client.delete(
            "/income/user/{}/".format(created_income.data["id"])
        )
        response2 = self.client.delete(
            "/income/user/{}/".format(created_income.data["id"])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)


# Create your tests here.
