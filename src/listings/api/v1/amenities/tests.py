from django.shortcuts import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_403_FORBIDDEN,
)

from core.models import Reference
from core.api.tests import BaseAPITest

from ....models import Amenity, Category


class Amenities(BaseAPITest):
    """
    Testing amenities endpoint
    """

    def test_create_amenity_no_auth(self) -> None:
        # Create new amenity without authentication
        response = self.client.post(
            reverse("listings:api_amenities"),
            {
                Reference.Field.name: "newAmenity",
                Reference.Field.description: "newAmenity description",
                Amenity.Field.category: 1
            },
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_create_amenity_standard_user(self) -> None:
        # Login with standard account
        self.engage_user()

        # Create new tag as standard user
        response = self.client.post(
            reverse("listings:api_amenities"),
            {
                Reference.Field.name: "newAmenity",
                Reference.Field.description: "newAmenity description",
            },
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_create_amenity_admin(self) -> None:
        # Login with standard account
        self.engage_admin()

        category_id = Category.objects.create(name="Test category").id

        # Create new amenity as standard user
        response = self.client.post(
            reverse("listings:api_amenities"),
            {
                Reference.Field.name: "newAmenity",
                Reference.Field.description: "newAmenity description",
                Amenity.Field.category: category_id
            },
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_201_CREATED
        )

    def test_list_amenities(self) -> None:
        category_object = Category.objects.create(name="Test category")
        for cat_index in range(0, 5):
            # Create test amenity objects
            Amenity.objects.create(
                name="Test{}".format(cat_index),
                description="{} amenity description".format(cat_index),
                category=category_object
                )

        # Getting amenities list without authentication
        response = self.client.get(
            reverse("listings:api_amenities")
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


class AmenityDetails(BaseAPITest):
    """
    Testing single amenity instance scenarios
    """

    def setUp(self) -> None:
        # Create test amenity object
        self.category_object = Category.objects.create(
            name="Test category"
        )
        Amenity.objects.create(
            name="Test",
            description="Test amenity description",
            category=self.category_object
        )

    def test_get_amenity_no_auth(self) -> None:
        # Create new amenity without authentication
        response = self.client.get(
            reverse(
                "listings:api_amenity_details",
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

    def test_update_amenity_no_auth(self) -> None:
        # Update amenity without authentication
        response = self.client.patch(
            reverse(
                "listings:api_amenity_details",
                kwargs={
                    Reference.Field.name: "Test"
                }
            ),
            {
                Reference.Field.name: "newAmenity",
                Reference.Field.description: "newAmenity description",
                Amenity.Field.category: self.category_object.id
            },
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_delete_amenity_no_auth(self) -> None:
        # Delete amenity without authentication
        response = self.client.delete(
            reverse(
                "listings:api_amenity_details",
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

    def test_update_amenity_standard_user(self) -> None:
        # Working as a standard user
        self.engage_user()

        # Update amenity
        response = self.client.patch(
            reverse(
                "listings:api_amenity_details",
                kwargs={
                    Reference.Field.name: "Test"
                }
            ),
            {
                Reference.Field.name: "newTest",
                Reference.Field.description: "newTest description",
                Amenity.Field.category: self.category_object.id
            },
            format="json"
        )

        # Check results through response code
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_delete_amenity_standard_user(self) -> None:
        # Working as a standard user
        self.engage_user()

        # Delete amenity
        response = self.client.delete(
            reverse(
                "listings:api_amenity_details",
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

    def test_update_amenity_admin(self) -> None:
        # Working as an admin
        self.engage_admin()

        # Update amenity
        response = self.client.patch(
            reverse(
                "listings:api_amenity_details",
                kwargs={
                    Reference.Field.name: "Test"
                }
            ),
            {
                Reference.Field.name: "newTest",
                Reference.Field.description: "newTest description",
                Amenity.Field.category: self.category_object.id
            },
            format="json"
        )

        # Check results through response code
        self.assertEqual(
            response.status_code,
            HTTP_200_OK
        )

    def test_delete_amenity_admin(self) -> None:
        # Working as an admin
        self.engage_admin()

        # Delete amenity
        response = self.client.delete(
            reverse(
                "listings:api_amenity_details",
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
