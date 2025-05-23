from django.shortcuts import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_403_FORBIDDEN,
)

from core.api.tests import BaseAPITest

from ....models import Tag


class Tags(BaseAPITest):
    """
    Testing tag lifecycle scenarios
    """

    def test_create_tag_no_auth(self) -> None:
        # Create new tag without authentication
        response = self.client.post(
            reverse("blog:api_tags"),
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

    def test_create_tag_standard_user(self) -> None:
        # Working as a standard user
        self.engage_user()

        # Create new tag as standard user
        response = self.client.post(
            reverse("blog:api_tags"),
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

    def test_create_tag_admin(self) -> None:
        # Working as an admin
        self.engage_admin()

        # Create new tag as standard user
        response = self.client.post(
            reverse("blog:api_tags"),
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

    def test_list_tags(self) -> None:
        # Create test tag object
        Tag.objects.create(
            name="Test",
            description="Test tag description"
        )

        # Getting tags list without authentication
        response = self.client.get(
            reverse("blog:api_tags")
        )

        # Check results through response code and content
        self.assertEqual(
            response.status_code,
            HTTP_200_OK
        )
        self.assertContains(
            response, "Test"
        )


class TagDetails(BaseAPITest):
    """
    Testing single tag instance lifecycle scenarios
    """

    def setUp(self) -> None:
        # Create test tag object
        Tag.objects.create(
            name="Test",
            description="Test tag description"
        )

    def test_get_tag_no_auth(self) -> None:
        # Create new tag without authentication
        response = self.client.get(
            reverse(
                "blog:api_tag_details",
                kwargs={
                    Tag.Field.name: "Test"
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

    def test_update_tag_no_auth(self) -> None:
        # Update tag without authentication
        response = self.client.patch(
            reverse(
                "blog:api_tag_details",
                kwargs={
                    Tag.Field.name: "Test"
                }
            ),
            {
                Tag.Field.name: "newTest",
                Tag.Field.description: "newTest description",
            },
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_delete_tag_no_auth(self) -> None:
        # Delete tag without authentication
        response = self.client.delete(
            reverse(
                "blog:api_tag_details",
                kwargs={
                    Tag.Field.name: "Test"
                }
            )
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_update_tag_standard_user(self) -> None:
        # Working as a standard user
        self.engage_user()

        # Update tag
        response = self.client.patch(
            reverse(
                "blog:api_tag_details",
                kwargs={
                    Tag.Field.name: "Test"
                }
            ),
            {
                Tag.Field.name: "newTest",
                Tag.Field.description: "newTest description",
            },
            format="json"
        )

        # Check results through response code
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_delete_tag_standard_user(self) -> None:
        # Working as a standard user
        self.engage_user()

        # Delete tag
        response = self.client.delete(
            reverse(
                "blog:api_tag_details",
                kwargs={
                    Tag.Field.name: "Test"
                }
            )
        )

        # Check results through response code
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_update_tag_admin(self) -> None:
        # Working as an admin
        self.engage_admin()

        # Update tag
        response = self.client.patch(
            reverse(
                "blog:api_tag_details",
                kwargs={
                    Tag.Field.name: "Test"
                }
            ),
            {
                Tag.Field.name: "newTest",
                Tag.Field.description: "newTest description",
            },
            format="json"
        )

        # Check results through response code
        self.assertEqual(
            response.status_code,
            HTTP_200_OK
        )

    def test_delete_tag_admin(self) -> None:
        # Working as an admin
        self.engage_admin()

        # Update tag
        response = self.client.delete(
            reverse(
                "blog:api_tag_details",
                kwargs={
                    Tag.Field.name: "Test"
                }
            )
        )

        # Check results through response code
        self.assertEqual(
            response.status_code,
            HTTP_204_NO_CONTENT
        )
