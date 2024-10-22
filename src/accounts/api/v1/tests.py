from django.urls import reverse

from rest_framework.exceptions import ErrorDetail
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY
)
from rest_framework.test import APITestCase

from ...constants import (
    ERROR_MSG_DUPLICATE_MAIL,
    ERROR_MSG_DIFFERENT_PASSWORDS
)
from ...models import Account
from tests.user_data import good_account

email = good_account.get(Account.Field.email)
password = good_account.get(Account.Field.password)


class CreateAccounts(APITestCase):
    """
    Testing accounts list and creation process
    """
    def create_good_account(self):
        # Create user though API call
        response = self.client.post(
            reverse("rest_accounts"),
            {
                Account.Field.email: email,
                Account.Field.password1: password,
                Account.Field.password2: password
            },
            format="json"
        )

        return response

    def test_create_user_no_email(self):
        # Create user though API call
        response = self.client.post(
            reverse("rest_accounts"),
            {
                Account.Field.password1: password,
                Account.Field.password2: password
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
            reverse("rest_accounts"),
            {
                Account.Field.email: email
            },
            format="json"
        )

        # Check result through response code
        self.assertEqual(
            response.status_code,
            HTTP_422_UNPROCESSABLE_ENTITY
        )
        self.assertIn(
            Account.Field.password1,
            response.data
        )
        self.assertIn(
            Account.Field.password2,
            response.data
        )

    def test_create_user_different_passwords(self):
        # Create user though API call
        response = self.client.post(
            reverse("rest_accounts"),
            {
                Account.Field.email: email,
                Account.Field.password1: password,
                Account.Field.password2: password.upper()

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


class ViewAccounts(APITestCase):
    """Testing different cases for accounts info access"""
    def setUp(self) -> None:
        # create test account
        Account.objects.create_user(
            email=email,
            password=password
        )

    def test_get_accounts_list_no_auth(self):
        # checking accounts list access without authentication
        response = self.client.get(reverse("rest_accounts"))

        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_get_accounts_list_no_admin(self):
        try:
            # login as a simple user
            user = Account.objects.get(id=1)
            self.client.force_login(user)

            # try to get all accounts list
            response = self.client.get(reverse("rest_accounts"))
            self.assertEqual(
                response.status_code,
                HTTP_403_FORBIDDEN
            )
        except Account.DoesNotExist:
            pass

    def test_get_accounts_list_admin(self):
        # checking accounts list access with admin privileges
        # create admin user
        admin = Account.objects.create_superuser(
            email="admin"+email,
            password=password
        )

        # login with admin credentials
        self.client.force_authenticate(admin)

        # now try to obtain users list
        response = self.client.get(reverse("rest_accounts"))
        self.assertEqual(
            response.status_code,
            HTTP_200_OK
        )

        # checking accounts number (admin + user = 2)
        self.assertEqual(
            len(response.data),
            2
        )

    def test_get_account_details(self):
        # getting the last registered account
        last_account = Account.objects.latest(
            Account.Field.date_joined
        )
        if last_account:
            # and checking its details
            response = self.client.get(
                reverse(
                    "rest_account_details",
                    args=(last_account.id,)
                )
            )
            self.assertEqual(
                response.status_code,
                HTTP_200_OK
            )
            self.assertIn(
                Account.Field.email,
                response.data
            )
            self.assertEqual(
                response.data.get(Account.Field.email),
                email
            )

    def test_get_wrong_account_details(self):
        # checking account details access
        response = self.client.get(
            reverse(
                "rest_account_details",
                args=(100,)
            )
        )
        self.assertEqual(
            response.status_code,
            HTTP_404_NOT_FOUND
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
                Account.Field.email: email,
                Account.Field.password: password
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
