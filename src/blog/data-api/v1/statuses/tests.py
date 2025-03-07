from django.shortcuts import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_403_FORBIDDEN,
)
from rest_framework.test import APITestCase

from accounts.models import Account
from tests.data import good_account

from ....models import Status

email = good_account.get(Account.Field.email)
password = good_account.get(Account.Field.password)


class Statuses(APITestCase):
    """
    Testing status lifecycle scenarios
    """

    def engage_user(self):
        # Create and login as standard user
        account = Account.objects.create_user(
            email=email,
            password=password
        )

        # Login with standard account
        self.client.force_login(account)

    def engage_admin(self):
        # Create admin account
        account = Account.objects.create_superuser(
            email="admin-{}".format(email),
            password=password
        )

        # Login with admin account
        self.client.force_login(account)

    def test_create_status_no_auth(self):
        # Create new status without authentication
        response = self.client.post(
            reverse("blog_api_statuses"),
            {
                Status.Field.name: "newStatus",
                Status.Field.description: "newStatus description",
            },
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_create_status_standard_user(self):
        # Login with standard account
        self.engage_user()

        # Create new tag as standard user
        response = self.client.post(
            reverse("blog_api_statuses"),
            {
                Status.Field.name: "newStatus",
                Status.Field.description: "newStatus description",
            },
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_create_status_admin(self):
        # Login with standard account
        self.engage_admin()

        # Create new status as standard user
        response = self.client.post(
            reverse("blog_api_statuses"),
            {
                Status.Field.name: "newStatus",
                Status.Field.description: "newStatus description",
            },
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_201_CREATED
        )

    def test_list_statuses(self):
        # Create test status object
        Status.objects.create(
            name="Test",
            description="Test status description",
            is_initial=True
        )

        # Getting statuses list without authentication
        response = self.client.get(
            reverse("blog_api_statuses")
        )

        # Check results through response code and content
        self.assertEqual(
            response.status_code,
            HTTP_200_OK
        )
        self.assertContains(
            response, "Test"
        )


class StatusDetails(APITestCase):
    """
    Testing single status instance lifecycle scenarios
    """

    def setUp(self) -> None:
        # Create test status object
        Status.objects.create(
            name="Test",
            description="Test status description"
        )

    def engage_user(self):
        # Create and login as standard user
        account = Account.objects.create_user(
            email=email,
            password=password
        )

        # Login with standard account
        self.client.force_login(account)

    def engage_admin(self):
        # Create admin account
        account = Account.objects.create_superuser(
            email="admin-{}".format(email),
            password=password
        )

        # Login with admin account
        self.client.force_login(account)

    def test_get_status_no_auth(self):
        # Create new status without authentication
        response = self.client.get(
            reverse(
                "blog_api_status_details",
                kwargs={
                    Status.Field.name: "Test"
                }
            )
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_200_OK
        )

        self.assertContains(
            response, "Test"
        )

    def test_update_status_no_auth(self):
        # Update status without authentication
        response = self.client.patch(
            reverse(
                "blog_api_status_details",
                kwargs={
                    Status.Field.name: "Test"
                }
            ),
            {
                Status.Field.name: "newStatus",
                Status.Field.description: "newStatus description",
                Status.Field.is_initial: True
            },
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_delete_status_no_auth(self):
        # Delete status without authentication
        response = self.client.delete(
            reverse(
                "blog_api_status_details",
                kwargs={
                    Status.Field.name: "Test"
                }
            )
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_update_status_standard_user(self):
        # Working as a standard user
        self.engage_user()

        # Update status
        response = self.client.patch(
            reverse(
                "blog_api_status_details",
                kwargs={
                    Status.Field.name: "Test"
                }
            ),
            {
                Status.Field.name: "newTest",
                Status.Field.description: "newTest description",
                Status.Field.is_initial: True
            },
            format="json"
        )

        # Check results through response code
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_delete_status_standard_user(self):
        # Working as a standard user
        self.engage_user()

        # Delete status
        response = self.client.delete(
            reverse(
                "blog_api_status_details",
                kwargs={
                    Status.Field.name: "Test"
                }
            )
        )

        # Check results through response code
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_update_status_admin(self):
        # Working as an admin
        self.engage_admin()

        # Update status
        response = self.client.patch(
            reverse(
                "blog_api_status_details",
                kwargs={
                    Status.Field.name: "Test"
                }
            ),
            {
                Status.Field.name: "newTest",
                Status.Field.description: "newTest description",
                Status.Field.is_initial: True
            },
            format="json"
        )

        # Check results through response code
        self.assertEqual(
            response.status_code,
            HTTP_200_OK
        )

    def test_delete_status_admin(self):
        # Working as an admin
        self.engage_admin()

        # Delete status
        response = self.client.delete(
            reverse(
                "blog_api_status_details",
                kwargs={
                    Status.Field.name: "Test"
                }
            )
        )

        # Check results through response code
        self.assertEqual(
            response.status_code,
            HTTP_204_NO_CONTENT
        )
