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

from tests.data import good_user

from ...models import Company
from ...tests import company_data

User = get_user_model()


class CompanyTest(TestCase):
    """

    """

    def setUp(self) -> None:
        """
        Pre-create some user accounts
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

    def test_create_company_no_auth(self) -> None:
        # Check if company can be created by non-authenticated user

        response = self.client.post(
            reverse("contacts:api_company"),
            {},
            format="json"
        )
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_create_company_as_standard_user(self) -> None:
        # Check if company can be created by standard user
        self.client.force_login(self.standard_user)

        response = self.client.post(
            reverse("contacts:api_company"),
            {},
            format="json"
        )
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_create_no_full_name(self) -> None:
        # Check if new post can be created company name
        self.client.force_login(self.admin_user)

        bad_data = company_data.copy()
        del bad_data[Company.Field.full_name]
        response = self.client.post(
            reverse("contacts:api_company"),
            bad_data,
            format="json"
            )
        self.assertEqual(
            response.status_code,
            HTTP_422_UNPROCESSABLE_ENTITY
            )

    def test_create_empty_full_name(self) -> None:
        # Check if new post can be created company name
        self.client.force_login(self.admin_user)

        bad_data = company_data.copy()
        bad_data[Company.Field.full_name] = ""
        response = self.client.post(
            reverse("contacts:api_company"),
            bad_data,
            format="json"
            )
        self.assertEqual(
            response.status_code,
            HTTP_422_UNPROCESSABLE_ENTITY
            )

    def test_create_company(self) -> None:
        # Check if new post can be created company name
        self.client.force_login(self.admin_user)

        response = self.client.post(
            reverse("contacts:api_company"),
            company_data,
            format="json"
            )
        self.assertEqual(
            response.status_code,
            HTTP_201_CREATED
            )

    def test_get_company(self) -> None:

        Company.objects.create(**company_data).save()

        response = self.client.get(
            reverse("contacts:api_company"),
            company_data,
            format="json"
            )
        self.assertEqual(
            response.status_code,
            HTTP_200_OK
            )
        for key, value in company_data.items():
            self.assertEqual(
                response.data.get(key),
                value
            )

    def test_patch_empty_full_name(self) -> None:
        # Check if new post can be created company name
        self.client.force_login(self.admin_user)
        Company.objects.create(**company_data).save()

        bad_data = company_data.copy()
        bad_data[Company.Field.full_name] = ""

        response = self.client.patch(
            reverse("contacts:api_company"),
            bad_data,
            content_type="application/json",
            )
        self.assertEqual(
            response.status_code,
            HTTP_422_UNPROCESSABLE_ENTITY
            )

    def test_patch(self) -> None:
        # Check if new post can be created company name
        Company.objects.create(**company_data).save()
        self.client.force_login(self.admin_user)

        new_data = {
            key: "new_{}".format(value) for key, value in company_data.items()
        }

        response = self.client.patch(
            reverse("contacts:api_company"),
            new_data,
            content_type="application/json",
            )
        self.assertEqual(
            response.status_code,
            HTTP_200_OK
            )

        for key, value in new_data.items():
            self.assertEqual(
                Company.objects.all()[0].__getattribute__(key),
                value
            )

    def test_delete(self) -> None:
        # Check if new post can be created company name
        Company.objects.create(**company_data).save()
        self.client.force_login(self.admin_user)

        response = self.client.delete(
            reverse("contacts:api_company")
        )
        self.assertEqual(
            response.status_code,
            HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Company.objects.count(),
            0
        )
