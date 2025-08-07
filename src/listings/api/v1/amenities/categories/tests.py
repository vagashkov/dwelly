from django.shortcuts import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_403_FORBIDDEN,
)

from core.api.tests import BaseAPITest
from core.models import Reference

from .....models import Category


class Categories(BaseAPITest):
    """
    Testing categories endpoint
    """

    def test_create_category_no_auth(self) -> None:
        # Create new category without authentication
        response = self.client.post(
            reverse("listings:api_categories"),
            {
                Reference.Field.name: "newCategory",
                Reference.Field.description: "newCategory description",
            },
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_create_category_standard_user(self) -> None:
        # Login with standard account
        self.engage_user()

        # Create new tag as standard user
        response = self.client.post(
            reverse("listings:api_categories"),
            {
                Reference.Field.name: "newCategory",
                Reference.Field.description: "newStatus description",
            },
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_create_category_admin(self) -> None:
        # Login with standard account
        self.engage_admin()

        # Create new category as standard user
        response = self.client.post(
            reverse("listings:api_categories"),
            {
                Reference.Field.name: "newCategory",
                Reference.Field.description: "newCategory description",
            },
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_201_CREATED
        )

    def test_list_categories(self) -> None:
        for cat_index in range(0, 5):
            # Create test category objects
            Category.objects.create(
                name="Test{}".format(cat_index),
                description="{} category description".format(cat_index)
                )

        # Getting categories list without authentication
        response = self.client.get(
            reverse("listings:api_categories")
        )

        # Check results for status code
        self.assertEqual(
            response.status_code,
            HTTP_200_OK
        )
        # Check results for correct data
        self.assertEqual(
            len(response.data),
            5
        )
        for cat_index in range(0, 5):
            self.assertContains(
                response, "Test{}".format(cat_index)
                )


class CategoryDetails(BaseAPITest):
    """
    Testing single category instance scenarios
    """

    def setUp(self) -> None:
        # Create test category object
        Category.objects.create(
            name="Test",
            description="Test category description"
        )

    def test_get_category_no_auth(self) -> None:
        # Create new category without authentication
        response = self.client.get(
            reverse(
                "listings:api_category_details",
                kwargs={
                    Reference.Field.name: "Test"
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

    def test_update_category_no_auth(self) -> None:
        # Update category without authentication
        response = self.client.patch(
            reverse(
                "listings:api_category_details",
                kwargs={
                    Reference.Field.name: "Test"
                }
            ),
            {
                Reference.Field.name: "newCategory",
                Reference.Field.description: "newCategory description",
            },
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_delete_category_no_auth(self) -> None:
        # Delete category without authentication
        response = self.client.delete(
            reverse(
                "listings:api_category_details",
                kwargs={
                    Reference.Field.name: "Test"
                }
            )
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_update_category_standard_user(self) -> None:
        # Working as a standard user
        self.engage_user()

        # Update category
        response = self.client.patch(
            reverse(
                "listings:api_category_details",
                kwargs={
                    Reference.Field.name: "Test"
                }
            ),
            {
                Reference.Field.name: "newTest",
                Reference.Field.description: "newTest description",
            },
            format="json"
        )

        # Check results through response code
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_delete_category_standard_user(self) -> None:
        # Working as a standard user
        self.engage_user()

        # Delete category
        response = self.client.delete(
            reverse(
                "listings:api_category_details",
                kwargs={
                    Reference.Field.name: "Test"
                }
            )
        )

        # Check results through response code
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_update_category_admin(self) -> None:
        # Working as an admin
        self.engage_admin()

        # Update category
        response = self.client.patch(
            reverse(
                "listings:api_category_details",
                kwargs={
                    Reference.Field.name: "Test"
                }
            ),
            {
                Reference.Field.name: "newTest",
                Reference.Field.description: "newTest description",
            },
            format="json"
        )

        # Check results through response code
        self.assertEqual(
            response.status_code,
            HTTP_200_OK
        )

    def test_delete_category_admin(self) -> None:
        # Working as an admin
        self.engage_admin()

        # Delete category
        response = self.client.delete(
            reverse(
                "listings:api_category_details",
                kwargs={
                    Reference.Field.name: "Test"
                }
            )
        )

        # Check results through response code
        self.assertEqual(
            response.status_code,
            HTTP_204_NO_CONTENT
        )
