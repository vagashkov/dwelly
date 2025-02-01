from django.urls import reverse

from rest_framework.exceptions import ErrorDetail
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_422_UNPROCESSABLE_ENTITY
)
from rest_framework.test import APITestCase

from ...constants import (
    ERROR_MSG_DUPLICATE_MAIL,
    ERROR_MSG_DIFFERENT_PASSWORDS
)
from ...models import Account
from ...tests import good_account


class CreateAccounts(APITestCase):
    """
    Testing accounts list and creation process
    """

    email = good_account.get(Account.Field.email)
    password = good_account.get(Account.Field.password)
    password1 = "{}1".format(Account.Field.password)
    password2 = "{}2".format(Account.Field.password)

    def create_good_account(self):
        # Create user though API call using valid data
        response = self.client.post(
            reverse("rest_register"),
            {
                Account.Field.email: self.email,
                self.password1: self.password,
                self.password2: self.password,
            },
            format="json"
        )

        return response

    def test_create_user_no_email(self):
        # Create user without email though API call
        response = self.client.post(
            reverse("rest_register"),
            {
                self.password1: self.password,
                self.password2: self.password,
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
        # Create user with no password though API call
        response = self.client.post(
            reverse("rest_register"),
            {
                Account.Field.email: self.email
            },
            format="json"
        )

        # Check result through response code
        self.assertEqual(
            response.status_code,
            HTTP_422_UNPROCESSABLE_ENTITY
        )
        self.assertIn(
            self.password1,
            response.data
        )
        self.assertIn(
            self.password2,
            response.data
        )

    def test_create_user_different_passwords(self):
        # Create user with non-matching passwords via API call
        response = self.client.post(
            reverse("rest_register"),
            {
                Account.Field.email: self.email,
                self.password1: self.password,
                self.password2: self.password.upper()

            },
            format="json"
        )

        # Check result through response code
        self.assertEqual(
            response.status_code,
            HTTP_422_UNPROCESSABLE_ENTITY
        )
        # check if custom error has been returned
        self.assertIn("non_field_errors", response.data)
        error_object = ErrorDetail(
            string=ERROR_MSG_DIFFERENT_PASSWORDS,
            code="invalid"
        )
        self.assertIn(
            error_object,
            response.data.get("non_field_errors")
        )

    def test_create_user_correct_data(self):
        # Try to create an account with correct data
        response = self.create_good_account()

        # Check result through response code
        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # Check if account was really created
        self.assertEqual(Account.objects.count(), 1)

        account = Account.objects.last()
        self.assertEqual(
            account.email,
            good_account.get(
                Account.Field.email
            )
        )

    def test_create_user_duplicate_email(self):
        # Try to create an account with correct data
        response = self.create_good_account()

        # Check result through response code
        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # Try to create one more account with the same data
        response = self.create_good_account()

        # Check result through response code
        self.assertEqual(response.status_code, HTTP_422_UNPROCESSABLE_ENTITY)

        # check if custom error has been returned
        self.assertIn(
            Account.Field.email,
            response.data
        )
        error_object = ErrorDetail(
            string=ERROR_MSG_DUPLICATE_MAIL,
            code="invalid"
        )
        self.assertIn(
            error_object,
            response.data.get(
                Account.Field.email
            )
        )
