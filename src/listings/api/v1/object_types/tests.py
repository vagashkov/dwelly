from django.shortcuts import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_403_FORBIDDEN,
)

from core.models import Reference
from core.api.tests import BaseAPITest

from ....models import ObjectType


class ObjectTypes(BaseAPITest):
    """
    Testing object types endpoint
    """

    def test_create_object_type_no_auth(self) -> None:
        # Create new object type without authentication
        response = self.client.post(
            reverse("listings:api_object_types"),
            {
                Reference.Field.name: "newObjectType",
                Reference.Field.description: "newObjectType description"
            },
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_create_object_type_standard_user(self) -> None:
        # Login with standard account
        self.engage_user()

        # Create new tag as standard user
        response = self.client.post(
            reverse("listings:api_object_types"),
            {
                Reference.Field.name: "newObjectType",
                Reference.Field.description: "newObjectType description",
            },
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_create_object_type_admin(self) -> None:
        # Login with standard account
        self.engage_admin()

        # Create new object type as standard user
        response = self.client.post(
            reverse("listings:api_object_types"),
            {
                Reference.Field.name: "newObjectType",
                Reference.Field.description: "newObjectType description"
            },
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_201_CREATED
        )

    def test_list_object_types(self) -> None:
        for object_type_index in range(0, 5):
            # Create test object type objects
            ObjectType.objects.create(
                name="Test{}".format(object_type_index),
                description="{} object type description".format(
                    object_type_index
                )
            )

        # Getting object types list without authentication
        response = self.client.get(
            reverse("listings:api_object_types")
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


class ObjectTypeDetails(BaseAPITest):
    """
    Testing single object type instance scenarios
    """

    def setUp(self) -> None:
        ObjectType.objects.create(
            name="Test",
            description="Test object type description"
        )

    def test_get_object_type_no_auth(self) -> None:
        # Create new object type without authentication
        response = self.client.get(
            reverse(
                "listings:api_object_type_details",
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

    def test_update_object_type_no_auth(self) -> None:
        # Update object type without authentication
        response = self.client.patch(
            reverse(
                "listings:api_object_type_details",
                kwargs={
                    Reference.Field.name: "Test"
                }
            ),
            {
                Reference.Field.name: "newObjectType",
                Reference.Field.description: "newObjectType description"
            },
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_delete_object_type_no_auth(self) -> None:
        # Delete object type without authentication
        response = self.client.delete(
            reverse(
                "listings:api_object_type_details",
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

    def test_update_object_type_standard_user(self) -> None:
        # Working as a standard user
        self.engage_user()

        # Update object type
        response = self.client.patch(
            reverse(
                "listings:api_object_type_details",
                kwargs={
                    Reference.Field.name: "Test"
                }
            ),
            {
                Reference.Field.name: "newTest",
                Reference.Field.description: "newTest description"
            },
            format="json"
        )

        # Check results through response code
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_delete_object_type_standard_user(self) -> None:
        # Working as a standard user
        self.engage_user()

        # Delete object type
        response = self.client.delete(
            reverse(
                "listings:api_object_type_details",
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

    def test_update_object_type_admin(self) -> None:
        # Working as an admin
        self.engage_admin()

        # Update object type
        response = self.client.patch(
            reverse(
                "listings:api_object_type_details",
                kwargs={
                    Reference.Field.name: "Test"
                }
            ),
            {
                Reference.Field.name: "newTest",
                Reference.Field.description: "newTest description"
            },
            format="json"
        )

        # Check results through response code
        self.assertEqual(
            response.status_code,
            HTTP_200_OK
        )

    def test_delete_object_type_admin(self) -> None:
        # Working as an admin
        self.engage_admin()

        # Delete object type
        response = self.client.delete(
            reverse(
                "listings:api_object_type_details",
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
