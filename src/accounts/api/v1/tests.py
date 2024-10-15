from django.urls import reverse

from rest_framework.exceptions import ErrorDetail
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_422_UNPROCESSABLE_ENTITY
)
from rest_framework.test import APITestCase

from accounts.constants import ERROR_MSG_DIFFERENT_PASSWORDS
from accounts.models import Account
from tests.data import good_account

API_URL = "accounts/api/v1/{}"

email = good_account.get(Account.Field.email)
password = good_account.get(Account.Field.password)


class RegistrationTest(APITestCase):
    """
    Testing registration process with different kinds of data
    """

    def test_create_user_no_email(self):
        # Create user though API call
        response = self.client.post(
            reverse("rest_register"),
            {
                "password1": good_account.get(
                    Account.Field.password
                ),
                "password2": good_account.get(
                    Account.Field.password
                )
            },
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_422_UNPROCESSABLE_ENTITY
        )
        self.assertIn(
            Account.Field.email,
            response.data
        )

    def test_create_user_no_passwords(self):
        # Create user though API call
        response = self.client.post(
            reverse("rest_register"),
            {
                "email": good_account.get(
                    Account.Field.email
                ),
            },
            format="json"
        )

        # Check result through response code
        self.assertEqual(
            response.status_code,
            HTTP_422_UNPROCESSABLE_ENTITY
        )
        self.assertIn(
            "password1",
            response.data
        )
        self.assertIn(
            "password2",
            response.data
        )

    def test_create_user_different_passwords(self):
        # Create user though API call
        response = self.client.post(
            reverse("rest_register"),
            {
                "email": good_account.get(
                    Account.Field.email
                ),
                "password1": good_account.get(
                    Account.Field.password
                ),
                "password2": good_account.get(
                    Account.Field.password
                ).upper()

            },
            format="json"
        )

        # Check result through response code
        self.assertEqual(
            response.status_code,
            HTTP_422_UNPROCESSABLE_ENTITY
        )
        # check if custom error has beed returned
        self.assertIn("non_field_errors", response.data)
        error_object = ErrorDetail(
            string=ERROR_MSG_DIFFERENT_PASSWORDS,
            code="invalid"
        )
        self.assertIn(
            error_object,
            response.data.get("non_field_errors")
        )


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
