from datetime import date
from dateutil.relativedelta import relativedelta

from django.shortcuts import reverse

from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_403_FORBIDDEN,
    HTTP_422_UNPROCESSABLE_ENTITY
)

from ....models import Listing, PriceTag
from ..tests import BaseListingsAPITest
from .constants import (
    ERROR_KEY, ERROR_MSG_UNKNOWN_LISTING
)

good_price_tag = {
    PriceTag.Field.start_date: date.today(),
    PriceTag.Field.end_date: date.today() + relativedelta(months=1),
    PriceTag.Field.price: 100,
    PriceTag.Field.description: "Test price tag description"
}


class PriceTags(BaseListingsAPITest):
    """
    Test listing price tag lifecycle endpoints
    """

    def setUp(self) -> None:
        """

        :return:
        """
        self.good_listing_object = self.create_good_listing()

    def test_create_price_tag_no_auth(self) -> None:
        # Create new listing price tag without authentication
        response = self.client.post(
            reverse(
                "listings:api_listing_price_tags",
                kwargs={
                    Listing.Field.slug:
                        self.good_listing_object.slug
                }
            ),
            {},
            format="json"
        )

        # Check results through response code
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_create_price_tag_standard_user(self) -> None:
        # Working as a standard (non-admin) user
        self.engage_user()

        # Create new listing price_tag
        response = self.client.post(
            reverse(
                "listings:api_listing_price_tags",
                kwargs={
                    Listing.Field.slug:
                        self.good_listing_object.slug
                }
            ),
            {},
            format="json"
        )

        # Check results through response code
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_create_photo_no_required_field(self) -> None:
        # Working as an admin
        self.engage_admin()

        for key in good_price_tag.keys():
            data = good_price_tag.copy()
            del data[key]

            # Create new listing price tag
            response = self.client.post(
                reverse(
                    "listings:api_listing_price_tags",
                    kwargs={
                        Listing.Field.slug:
                        self.good_listing_object.slug
                        }
                    ),
                data,
                format="json"
                )

            # Check results through response code and error message
            self.assertEqual(
                response.status_code,
                HTTP_422_UNPROCESSABLE_ENTITY
            )

    def test_create_price_tag_unknown_listing(self) -> None:
        # Working as an admin
        self.engage_admin()

        # Create new listing price tag
        response = self.client.post(
            reverse(
                "listings:api_listing_price_tags",
                kwargs={
                    Listing.Field.slug: "000000"
                }
            ),
            good_price_tag,
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_422_UNPROCESSABLE_ENTITY
        )

        self.assertEqual(
             response.data.get(ERROR_KEY),
             ERROR_MSG_UNKNOWN_LISTING
        )

    def test_create_price_tag(self) -> None:
        # Working as an admin
        self.engage_admin()

        # Create new listing price tag
        response = self.client.post(
            reverse(
                "listings:api_listing_price_tags",
                kwargs={
                    Listing.Field.slug:
                        self.good_listing_object.slug
                }
            ),
            good_price_tag,
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_201_CREATED
        )

        self.assertEqual(
            response.data.get(PriceTag.Field.start_date),
            good_price_tag.get(PriceTag.Field.start_date).strftime("%Y-%m-%d")
        )
        self.assertEqual(
            response.data.get(PriceTag.Field.end_date),
            good_price_tag.get(PriceTag.Field.end_date).strftime("%Y-%m-%d")
        )
        self.assertEqual(
            response.data.get(PriceTag.Field.price),
            "{:.4f}".format(
                good_price_tag.get(PriceTag.Field.price)
            )
        )
        self.assertEqual(
            response.data.get(PriceTag.Field.description),
            good_price_tag.get(PriceTag.Field.description)
        )
