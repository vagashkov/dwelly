from django.shortcuts import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_403_FORBIDDEN,
)
from rest_framework.test import APITestCase

from accounts.models import Account
from tests.data import good_account

from ....models import Tag

email = good_account.get(Account.Field.email)
password = good_account.get(Account.Field.password)


class Tags(APITestCase):
    """
    Testing tag lifecycle scenarios
    """

    def test_create_tag_no_auth(self):
        # Create new tag without authentication
        response = self.client.post(
            reverse("blog_api_tags"),
            {
                Tag.Field.name: "newTag",
                Tag.Field.description: "newTag description",
            },
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_create_tag_standard_user(self):
        # Create standard account
        account = Account.objects.create_user(
            email=email,
            password=password
        )

        # Login with standard account
        self.client.force_login(account)

        # Create new tag as standard user
        response = self.client.post(
            reverse("blog_api_tags"),
            {
                Tag.Field.name: "newTag",
                Tag.Field.description: "newTag description",
            },
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_create_tag_admin(self):
        # Create standard account
        account = Account.objects.create_superuser(
            email="admin-{}".format(email),
            password=password
        )

        # Login with standard account
        self.client.force_login(account)

        # Create new tag as standard user
        response = self.client.post(
            reverse("blog_api_tags"),
            {
                Tag.Field.name: "newTag",
                Tag.Field.description: "newTag description",
            },
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_201_CREATED
        )

    def test_list_tags(self):
        # Create test tag object
        Tag.objects.create(
            name="Test tag",
            description="Test tag description"
        )

        # Getting tags list without authentication
        response = self.client.get(
            reverse("blog_api_tags")
        )

        # Check results through response code and content
        self.assertEqual(
            response.status_code,
            HTTP_200_OK
        )
        self.assertContains(
            response, "Test tag"
        )
