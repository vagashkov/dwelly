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

from ....models import Company, CompanyAddress
from ....tests import company_data, company_address

from .serializers import AddressSerializer

User = get_user_model()


class CompanyAddressTest(TestCase):
    """

    """

    def setUp(self) -> None:
        """
        Pre-create some posts to browse
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

        self.company = Company.objects.create(
            **company_data
        )

    def test_create_company_address_no_auth(self) -> None:
        # Check if company can be created by non-authenticated user

        response = self.client.post(
            reverse("contacts:api_company_addresses"),
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

    def test_create_address_bad_country(self) -> None:
        # Check if new post can be created company name
        self.client.force_login(self.admin_user)

        bad_data = company_address.copy()
        bad_data[CompanyAddress.Field.country] = "ZZ"
        bad_data[CompanyAddress.Field.company] = self.company
        response = self.client.post(
            reverse("contacts:api_company_addresses"),
            AddressSerializer(bad_data).data,
            format="json"
            )
        self.assertEqual(
            response.status_code,
            HTTP_422_UNPROCESSABLE_ENTITY
            )

    def test_create_address_(self) -> None:
        # Check if new post can be created company name
        self.client.force_login(self.admin_user)

        address = company_address.copy()
        address[CompanyAddress.Field.company] = self.company

        response = self.client.post(
            reverse("contacts:api_company_addresses"),
            AddressSerializer(address).data,
            format="json",
            content_type="application/json"
            )
        self.assertEqual(
            response.status_code,
            HTTP_201_CREATED
            )

    def test_get_address(self) -> None:
        address = company_address.copy()
        address[CompanyAddress.Field.company] = self.company

        CompanyAddress.objects.create(**address)

        response = self.client.get(
            reverse("contacts:api_company_addresses")
         )
        self.assertEqual(
             response.status_code,
             HTTP_200_OK
        )
        for key in company_address:
            self.assertEqual(
                response.data.get(key),
                company_address.get(key)
            )

    def test_patch_company_address(self) -> None:
        CompanyAddress.objects.create(
            **company_address,
            company=self.company
        ).save()
        self.client.force_login(self.admin_user)

        new_data = {
            key: "new{}".format(value)
            for key, value
            in company_address.items()
            if not key == CompanyAddress.Field.country
        }
        new_data[CompanyAddress.Field.country] = "GR"

        response = self.client.patch(
            reverse("contacts:api_company_addresses"),
            AddressSerializer(new_data).data,
            content_type="application/json",
            )
        self.assertEqual(
            response.status_code,
            HTTP_200_OK
            )

        for key, value in new_data.items():
            self.assertEqual(
                CompanyAddress.objects.all()[0].__getattribute__(key),
                value
            )

    def test_delete_company_address(self) -> None:
        CompanyAddress.objects.create(
            **company_address,
            company=self.company
        ).save()
        self.client.force_login(self.admin_user)

        response = self.client.delete(
            reverse("contacts:api_company_addresses")
        )
        self.assertEqual(
            response.status_code,
            HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            CompanyAddress.objects.count(),
            0
        )
