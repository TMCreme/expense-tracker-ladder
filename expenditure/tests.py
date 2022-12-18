"""
Test cases for the User's Expenditure Endpoints
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status


def create_user(**params):
    """Signup and return a new user"""
    return get_user_model().objects.create_user(**params)


class ExpenditureAPITests(TestCase):
    """Expenditure API Tests"""

    def setUp(self) -> None:
        self.client = APIClient()
        payload = {
            "email": "test@example.com",
            "password": "testpasswd123",
        }
        user = create_user(**payload)
        self.client.force_authenticate(user)

    def test_add_expenditure_success(self):
        """Add expenditure successfully"""

        payload = {
            "category": "transport",
            "name_of_item": "transport",
            "estimated_amount": 50
        }
        response = self.client.post("/expenditure/user/", payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertIn("category", response.data)
        self.assertIn("name_of_item", response.data)
        self.assertIn("estimated_amount", response.data)

    def test_add_expense_with_empty_name(self):
        """Add expense with empty string as name"""

        payload = {
            "category": "transport",
            "name_of_item": "",
            "estimated_amount": 50
        }
        response = self.client.post("/expenditure/user/", payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_expense_with_empty_amount(self):
        """Add expense with empty string as amount"""

        payload = {
            "category": "transport",
            "name_of_item": "transport",
            "estimated_amount": ""
        }

        response = self.client.post("/expenditure/user/", payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_expense(self):
        """Successfully retrieve user's expense"""

        payload = {
            "category": "transport",
            "name_of_item": "transport",
            "estimated_amount": 50
        }
        self.client.post("/expenditure/user/", payload)
        response = self.client.get("/expenditure/user/")
        data_size = len(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data_size, 1)

    def test_get_user_expense_with_no_data(self):
        """Retrieve user's expenditure with no data """

        # Create a record for a different user
        client2 = APIClient()
        user2_payload = {
            "email": "test2@example.com",
            "password": "testpas123",
        }
        user = create_user(**user2_payload)
        client2.force_authenticate(user)

        payload = {
            "category": "transport",
            "name_of_item": "transport",
            "estimated_amount": 50
        }
        client2.post("/expenditure/user/", payload)

        response = self.client.get("/expenditure/user/")

        data_size = len(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data_size, 0)

    def test_get_expense_by_id(self):
        """Retrieve an individual expenditure item"""

        payload = {
            "category": "transport",
            "name_of_item": "transport",
            "estimated_amount": 50
        }

        created_expense = self.client.post("/expenditure/user/", payload)

        response = self.client.get(
            "/expenditure/user/{}/".format(
                created_expense.data["id"]
                )
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data)
        self.assertIn("name_of_item", response.data)
        self.assertIn("estimated_amount", response.data)
        self.assertEqual(response.data, created_expense.data)

    def test_update_expense_item(self):
        """Update an Expense item with full payload"""

        payload = {
            "category": "transport",
            "name_of_item": "transport",
            "estimated_amount": 50
        }

        created_expense = self.client.post("/expenditure/user/", payload)

        response = self.client.put(
            "/expenditure/user/{}/".format(created_expense.data["id"]),
            {
                "category": "transport",
                "name_of_item": "transport",
                "estimated_amount": 100
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["name_of_item"],
            created_expense.data["name_of_item"]
        )
        self.assertEqual(response.data["estimated_amount"], 100)

    def test_update_put_with_partial_data(self):
        """Test Put request with partial data"""

        payload = {
            "category": "transport",
            "name_of_item": "transport",
            "estimated_amount": 50
        }

        created_expense = self.client.post("/expenditure/user/", payload)

        response = self.client.put(
            "/expenditure/user/{}/".format(created_expense.data["id"]),
            {
                "category": "transport",
                "estimated_amount": 100
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_patch_with_partial(self):
        """Partial update payload for patch method"""

        payload = {
            "category": "transport",
            "name_of_item": "transport",
            "estimated_amount": 50
        }

        created_expense = self.client.post("/expenditure/user/", payload)

        response = self.client.patch(
            "/expenditure/user/{}/".format(created_expense.data["id"]),
            {
                "category": "transport",
                "estimated_amount": 100
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["name_of_item"],
            created_expense.data["name_of_item"]
        )
        self.assertEqual(response.data["estimated_amount"], 100)

    def test_delete_expense_data(self):
        """Delete an expense item"""

        payload = {
            "category": "transport",
            "name_of_item": "transport",
            "estimated_amount": 50
        }

        created_expense = self.client.post("/expenditure/user/", payload)

        response = self.client.delete(
            "/expenditure/user/{}/".format(created_expense.data["id"])
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_an_already_deleted_item(self):
        """Test multiple delete on an item"""

        payload = {
            "category": "transport",
            "name_of_item": "transport",
            "estimated_amount": 50
        }

        created_expense = self.client.post("/expenditure/user/", payload)

        response = self.client.delete(
            "/expenditure/user/{}/".format(created_expense.data["id"])
        )

        response2 = self.client.delete(
            "/expenditure/user/{}/".format(created_expense.data["id"])
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)


# Create your tests here.
