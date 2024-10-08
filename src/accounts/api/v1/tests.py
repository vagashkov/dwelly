from django.urls import reverse

from rest_framework.status import HTTP_200_OK
from rest_framework.test import APITestCase

from accounts.models import Account
from tests.data import good_account

API_URL = "accounts/api/v1/{}"

email = good_account.get(Account.Field.email)
password = good_account.get(Account.Field.password)


class LoginTest(APITestCase):
    """
    Testing login/logout endpoints:
    """

    def setUp(self):
        Account.objects.create_user(
            email=email,
            password=password
            )

    def test_login_process(self):
        """
        Test user login process via API
        :return:
        """

        self.response = self.client.post(
            reverse("rest_login"),
            {
                "email": email,
                "password": password
            }
        )

        # after successful authorization token
        # should be returned
        self.assertEqual(self.response.status_code, HTTP_200_OK)
        self.assertIn("key", self.response.data)

    def test_logout_process(self):
        """
        Test user logout process via API
        :return:
        """

        self.response = self.client.post(
            reverse("rest_logout"),
        )

        # after successful logout specific message should be returned
        self.assertEqual(self.response.status_code, HTTP_200_OK)
        self.assertIn("detail", self.response.data)
        self.assertEqual(
            self.response.data.get("detail"),
            "Successfully logged out."
        )
