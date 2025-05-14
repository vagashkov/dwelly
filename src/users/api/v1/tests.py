from django.urls import reverse

from rest_framework.exceptions import ErrorDetail
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY
)
from rest_framework.test import APITestCase

from tests.test_data import good_user, good_profile

from ...constants import (
    ERROR_MSG_DUPLICATE_MAIL,
    ERROR_MSG_DIFFERENT_PASSWORDS
)
from ...models import User, Profile


email = good_user.get(User.Field.email)
password = good_user.get(User.Field.password)


class CreateUsers(APITestCase):
    """
    Testing accounts list and creation process
    """

    password1 = "{}1".format(User.Field.password)
    password2 = "{}2".format(User.Field.password)

    def create_good_user(self) -> Response:
        # Create user though API call using valid data
        response = self.client.post(
            reverse("rest_register"),
            {
                User.Field.email: email,
                self.password1: password,
                self.password2: password,
            },
            format="json"
        )

        return response

    def test_create_user_no_email(self) -> None:
        # Create user without email though API call
        response = self.client.post(
            reverse("rest_register"),
            {
                self.password1: password,
                self.password2: password,
            },
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_422_UNPROCESSABLE_ENTITY
        )
        self.assertIn(
            User.Field.email,
            response.data
        )

    def test_create_user_no_passwords(self) -> None:
        # Create user with no password though API call
        response = self.client.post(
            reverse("rest_register"),
            {
                User.Field.email: email
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

    def test_create_user_different_passwords(self) -> None:
        # Create user with non-matching passwords via API call
        response = self.client.post(
            reverse("rest_register"),
            {
                User.Field.email: email,
                self.password1: password,
                self.password2: password.upper()

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

    def test_create_user_correct_data(self) -> None:
        # Try to create an account with correct data
        response = self.create_good_user()

        # Check result through response code
        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # Check if account was really created
        self.assertEqual(User.objects.count(), 1)

        account = User.objects.last()
        self.assertEqual(
            account.email,
            good_user.get(
                User.Field.email
            )
        )

    def test_create_user_duplicate_email(self) -> None:
        # Try to create an account with correct data
        response = self.create_good_user()

        # Check result through response code
        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # Try to create one more account with the same data
        response = self.create_good_user()

        # Check result through response code
        self.assertEqual(response.status_code, HTTP_422_UNPROCESSABLE_ENTITY)

        # check if custom error has been returned
        self.assertIn(
            User.Field.email,
            response.data
        )
        error_object = ErrorDetail(
            string=ERROR_MSG_DUPLICATE_MAIL,
            code="invalid"
        )
        self.assertIn(
            error_object,
            response.data.get(
                User.Field.email
            )
        )


class ProfileTest(APITestCase):
    """Testing different cases for profiles info access"""

    def setUp(self) -> None:
        # create test account
        self.user = User.objects.create_user(
            email=email,
            password=password
        )
        # create admin user
        self.admin = User.objects.create_superuser(
            email="admin" + email,
            password=password
        )

    def test_get_profiles_list_no_auth(self) -> None:
        # checking profiles list access without authentication
        response = self.client.get(reverse("rest_profiles"))

        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_get_profiles_list_no_admin(self) -> None:
        # checking profiles list access as regular user
        self.client.force_login(self.user)
        response = self.client.get(reverse("rest_profiles"))

        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_get_profiles_list_admin(self) -> None:
        # checking profiles list access with admin privileges

        self.client.force_authenticate(self.admin)
        response = self.client.get(reverse("rest_profiles"))

        self.assertEqual(
            response.status_code,
            HTTP_200_OK
        )

        # checking profiles number (admin + user = 2)
        self.assertEqual(
            len(response.data),
            2
        )

    def test_get_profile_details_no_auth(self) -> None:
        # checking profiles details access without authentication
        response = self.client.get(
            reverse(
                 "rest_profile_details",
                 args=(self.admin.public_id,)
            )
        )
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_get_other_user_profile_details(self) -> None:
        # checking other user profile access

        second_user = User.objects.create_user(
            email="second_user@django.com",
            password=password
        )
        self.client.force_authenticate(second_user)

        # requesting another user profile
        response = self.client.get(
            reverse(
                "rest_profile_details",
                args=(self.user.public_id,)
            )
        )

        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
            )

    def test_get_profile_details_as_admin(self) -> None:
        # checking other user profile details  with admin credentials
        self.client.force_authenticate(self.admin)
        response = self.client.get(
            reverse(
                "rest_profile_details",
                args=(self.user.public_id,)
            )
        )

        self.assertEqual(
            response.status_code,
            HTTP_200_OK
        )

    def test_get_wrong_profile_details(self) -> None:
        # checking non-existing profile details

        self.client.force_authenticate(self.admin)
        response = self.client.get(
            reverse(
                "rest_profile_details",
                args=("999999",)
            )
        )
        self.assertEqual(
            response.status_code,
            HTTP_404_NOT_FOUND
        )

    def test_get_own_profile_no_auth(self) -> None:
        # checking profiles list access without authentication
        response = self.client.get(reverse("rest_user_profile"))

        self.assertEqual(
            response.status_code,
            HTTP_404_NOT_FOUND
        )

    def test_get_own_profile_details(self) -> None:
        # checking own profile access

        self.client.force_authenticate(self.user)
        response = self.client.get(
            reverse(
                "rest_user_profile"
            )
        )

        self.assertEqual(
            response.status_code,
            HTTP_200_OK
        )

        # verifying response content
        self.assertIn(
            Profile.Field.user,
            response.data
        )
        account = response.data.get(
            Profile.Field.user
        )
        self.assertEqual(
            account.get(User.Field.email),
            email
        )

    def test_update_own_profile_details(self) -> None:
        # checking own profile details update access

        self.client.force_authenticate(self.user)
        # try to update profile details
        response = self.client.patch(
            reverse(
                "rest_user_profile"
            ),
            data=good_profile
        )
        # check result
        self.assertEqual(
            response.status_code,
            HTTP_200_OK
        )

        # reload profile data one more time
        response = self.client.get(
            reverse(
                "rest_profile_details",
                args=(self.user.public_id,),
            )
        )

        # check if all the data was updated successfully
        for key in good_profile.keys():
            self.assertEqual(
                response.data.get(key),
                good_profile.get(key)
            )


class LoginTest(APITestCase):
    """
    Testing login/logout endpoints:
    """

    def setUp(self) -> None:
        User.objects.create_user(
            email=email,
            password=password
            )

    def test_login_process(self) -> None:
        """
        Test user login process via API
        :return:
        """

        self.response = self.client.post(
            reverse("rest_login"),
            {
                User.Field.email: email,
                User.Field.password: password
            }
        )

        # after successful authorization token should be returned
        self.assertEqual(self.response.status_code, HTTP_200_OK)
        self.assertIn("key", self.response.data)

    def test_logout_process(self) -> None:
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
