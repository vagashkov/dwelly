from django.shortcuts import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_403_FORBIDDEN,
)

from core.models import Reference
from core.api.tests import BaseAPITest

from ....models import HouseRule


class HouseRules(BaseAPITest):
    """
    Testing house rules endpoint
    """

    def test_create_house_rule_no_auth(self) -> None:
        # Create new house rule without authentication
        response = self.client.post(
            reverse("listings:api_house_rules"),
            {
                Reference.Field.name: "newHouseRule",
                Reference.Field.description: "newHouseRule description"
            },
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_create_house_rule_standard_user(self) -> None:
        # Login with standard account
        self.engage_user()

        # Create new tag as standard user
        response = self.client.post(
            reverse("listings:api_house_rules"),
            {
                Reference.Field.name: "newHouseRule",
                Reference.Field.description: "newHouseRule description",
            },
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_create_house_rule_admin(self) -> None:
        # Login with standard account
        self.engage_admin()

        # Create new house rule as standard user
        response = self.client.post(
            reverse("listings:api_house_rules"),
            {
                Reference.Field.name: "newHouseRule",
                Reference.Field.description: "newHouseRule description"
            },
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_201_CREATED
        )

    def test_list_house_rules(self) -> None:
        for house_rule_index in range(0, 5):
            # Create test house rule objects
            HouseRule.objects.create(
                name="Test{}".format(house_rule_index),
                description="{} house rule description".format(
                    house_rule_index
                )
            )

        # Getting house rules list without authentication
        response = self.client.get(
            reverse("listings:api_house_rules")
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


class HouseRuleDetails(BaseAPITest):
    """
    Testing single house rule instance scenarios
    """

    def setUp(self) -> None:
        HouseRule.objects.create(
            name="Test",
            description="Test house rule description"
        )

    def test_get_house_rule_no_auth(self) -> None:
        # Create new house rule without authentication
        response = self.client.get(
            reverse(
                "listings:api_house_rule_details",
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

    def test_update_house_rule_no_auth(self) -> None:
        # Update house rule without authentication
        response = self.client.patch(
            reverse(
                "listings:api_house_rule_details",
                kwargs={
                    Reference.Field.name: "Test"
                }
            ),
            {
                Reference.Field.name: "newHouseRule",
                Reference.Field.description: "newHouseRule description"
            },
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_delete_house_rule_no_auth(self) -> None:
        # Delete house rule without authentication
        response = self.client.delete(
            reverse(
                "listings:api_house_rule_details",
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

    def test_update_house_rule_standard_user(self) -> None:
        # Working as a standard user
        self.engage_user()

        # Update house rule
        response = self.client.patch(
            reverse(
                "listings:api_house_rule_details",
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

    def test_delete_house_rule_standard_user(self) -> None:
        # Working as a standard user
        self.engage_user()

        # Delete house rule
        response = self.client.delete(
            reverse(
                "listings:api_house_rule_details",
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

    def test_update_house_rule_admin(self) -> None:
        # Working as an admin
        self.engage_admin()

        # Update house rule
        response = self.client.patch(
            reverse(
                "listings:api_house_rule_details",
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

    def test_delete_house_rule_admin(self) -> None:
        # Working as an admin
        self.engage_admin()

        # Delete house rule
        response = self.client.delete(
            reverse(
                "listings:api_house_rule_details",
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
