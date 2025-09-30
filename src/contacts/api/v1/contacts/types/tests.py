from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.test import TestCase

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_403_FORBIDDEN,
    HTTP_422_UNPROCESSABLE_ENTITY
)

from core.models import Reference
from tests.data import good_user

from .....models import ContactType

User = get_user_model()

contact_type_data = {
    Reference.Field.name: "e-mail",
    Reference.Field.description: "Preferred contact type"
}


class ContactTypesTest(TestCase):
    """

    """

    def setUp(self) -> None:
        """
        Pre-create some users
        :return:
        """
        self.standard_user = User.objects.create(
            email=good_user.get(User.Field.email),
            password=good_user.get(User.Field.password)
        )

        self.admin_user = User.objects.create_superuser(
            email="admin{}".format(good_user.get(User.Field.email)),
            password=good_user.get(User.Field.password)
        )

    def test_create_contact_type_no_auth(self) -> None:
        # Check if contact type can be created by non-authenticated user
        response = self.client.post(
            reverse("contacts:api_company_contact_types"),
            contact_type_data,
            format="json",
            content_type="application/json"
        )
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_create_contact_type_as_standard_user(self) -> None:
        # Check if contact type can be created by standard user
        self.client.force_login(self.standard_user)

        response = self.client.post(
            reverse("contacts:api_company_contact_types"),
            contact_type_data,
            format="json",
            content_type="application/json"
        )
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_create_contact_type_no_name(self) -> None:
        # Check if new contact type can be created without name
        self.client.force_login(self.admin_user)

        bad_data = contact_type_data.copy()
        del bad_data[Reference.Field.name]

        response = self.client.post(
            reverse("contacts:api_company_contact_types"),
            bad_data,
            content_type="application/json"
        )
        self.assertEqual(
            response.status_code,
            HTTP_422_UNPROCESSABLE_ENTITY
        )

    def test_create_contact_type_empty_full_name(self) -> None:
        # Check if new contact type can be created with empty name
        self.client.force_login(self.admin_user)

        bad_data = contact_type_data.copy()
        bad_data[Reference.Field.name] = ""

        response = self.client.post(
            reverse("contacts:api_company_contact_types"),
            bad_data,
            content_type="application/json"
        )
        self.assertEqual(
            response.status_code,
            HTTP_422_UNPROCESSABLE_ENTITY
        )

    def test_create_valid_contact_type(self) -> None:
        self.client.force_login(self.admin_user)

        response = self.client.post(
            reverse("contacts:api_company_contact_types"),
            contact_type_data,
            content_type="application/json"
        )
        self.assertEqual(
            response.status_code,
            HTTP_201_CREATED
        )
        for key in contact_type_data:
            self.assertEqual(
                response.data.get(key),
                contact_type_data.get(key)
            )

    def test_create_contact_type_double(self) -> None:
        # Check if two contact types can have the same name
        ContactType.objects.create(**contact_type_data)

        self.client.force_login(self.admin_user)

        response = self.client.post(
            reverse("contacts:api_company_contact_types"),
            contact_type_data,
            content_type="application/json"
        )
        self.assertEqual(
            response.status_code,
            HTTP_422_UNPROCESSABLE_ENTITY
        )

    def test_get_contact_types(self) -> None:
        # Getting available contact types list
        for counter in range(5):
            ContactType.objects.create(
                name="{}{}".format(
                    contact_type_data.get(Reference.Field.name),
                    counter
                ),
                description="{}{}".format(
                    contact_type_data.get(Reference.Field.description),
                    counter
                )
            ).save()

        response = self.client.get(
            reverse("contacts:api_company_contact_types")
        )
        self.assertEqual(
            response.status_code,
            HTTP_200_OK
        )

        self.assertEqual(
            len(response.data.get("results")),
            5
        )

        for counter in range(5):
            self.assertTrue(
                filter(
                    lambda contact_type: contact_type.get(
                        Reference.Field.name
                    ) == "{}{}".format(
                        contact_type_data.get(
                            Reference.Field.name
                        ),
                        counter
                    ),
                    response.data.get("results")
                )
            )


class ContactTypeDetailsTest(TestCase):
    """
    Testing single contact type instance lifecycle scenarios
    """

    def setUp(self) -> None:
        # Create test contact type object
        ContactType.objects.create(
            **contact_type_data
        )

        self.standard_user = User.objects.create(
            email=good_user.get(User.Field.email),
            password=good_user.get(User.Field.password)
        )

        self.admin_user = User.objects.create_superuser(
            email="admin{}".format(good_user.get(User.Field.email)),
            password=good_user.get(User.Field.password)
        )

    def test_get_contact_type_no_auth(self) -> None:
        # Create new contact type without authentication
        response = self.client.get(
            reverse(
                "contacts:api_company_contact_type_details",
                kwargs={
                    ContactType.Field.name: contact_type_data.get(
                        Reference.Field.name
                    )
                }
            )
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_200_OK
        )

        self.assertEqual(
            response.data.get(Reference.Field.name),
            contact_type_data.get(Reference.Field.name)
        )

        self.assertEqual(
            response.data.get(Reference.Field.description),
            contact_type_data.get(Reference.Field.description)
        )

    def test_update_contact_type_no_auth(self) -> None:
        # Update contact type without authentication
        response = self.client.patch(
            reverse(
                "contacts:api_company_contact_type_details",
                kwargs={
                    ContactType.Field.name: contact_type_data.get(
                        Reference.Field.name
                    )
                }
            ),
            {
                Reference.Field.name: "newType",
                Reference.Field.description: "newType description",
            },
            content_type="application/json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_delete_contact_type_no_auth(self) -> None:
        # Delete contact type without authentication
        response = self.client.delete(
            reverse(
                "contacts:api_company_contact_type_details",
                kwargs={
                    ContactType.Field.name: contact_type_data.get(
                        Reference.Field.name
                    )
                }
            )
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_update_contact_type_standard_user(self) -> None:
        # Update contact type as standard user
        self.client.force_login(self.standard_user)
        response = self.client.patch(
            reverse(
                "contacts:api_company_contact_type_details",
                kwargs={
                    ContactType.Field.name: contact_type_data.get(
                        Reference.Field.name
                    )
                }
            ),
            {
                Reference.Field.name: "newType",
                Reference.Field.description: "newType description",
            },
            content_type="application/json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_delete_contact_type_standard_user(self) -> None:
        # Delete contact type as standard user
        self.client.force_login(self.standard_user)

        response = self.client.delete(
            reverse(
                "contacts:api_company_contact_type_details",
                kwargs={
                    ContactType.Field.name: contact_type_data.get(
                        Reference.Field.name
                    )
                }
            )
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_update_contact_type_admin(self) -> None:
        # Update contact type as admin user
        self.client.force_login(self.admin_user)
        response = self.client.patch(
            reverse(
                "contacts:api_company_contact_type_details",
                kwargs={
                    ContactType.Field.name: contact_type_data.get(
                        Reference.Field.name
                    )
                }
            ),
            {
                Reference.Field.name: "newType",
                Reference.Field.description: "newType description",
            },
            content_type="application/json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_200_OK
        )

        self.assertTrue(
            ContactType.objects.filter(
                name="newType"
            ).exists()
        )

        self.assertEqual(
            ContactType.objects.get(
                name="newType"
            ).description,
            "newType description"
        )

    def test_delete_contact_type_admin(self) -> None:
        # Update contact type as admin user
        self.client.force_login(self.admin_user)
        response = self.client.delete(
            reverse(
                "contacts:api_company_contact_type_details",
                kwargs={
                    ContactType.Field.name: contact_type_data.get(
                        Reference.Field.name
                    )
                }
            )
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_204_NO_CONTENT
        )
