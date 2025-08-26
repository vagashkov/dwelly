from datetime import date
from dateutil.relativedelta import relativedelta

from django.shortcuts import reverse

from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_403_FORBIDDEN,
    HTTP_422_UNPROCESSABLE_ENTITY
)

from tests.data import good_price_tag
from tests.objects import create_good_listing

from ....models import Listing, PriceTag, DayRate

from ..constants import (
    ERROR_KEY, ERROR_MSG_UNKNOWN_LISTING
)
from ..tests import BaseListingsAPITest


class PriceTags(BaseListingsAPITest):
    """
    Test listing price tag lifecycle endpoints
    """

    def setUp(self) -> None:
        """

        :return:
        """
        self.good_listing_object = create_good_listing()

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

    def test_create_price_tag_no_required_field(self) -> None:
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

    def test_get_listing_price_tags(self) -> None:
        # Append price tags
        price_tags = list()
        for index in range(5):
            price_tag = PriceTag.objects.create(
                listing=self.good_listing_object,
                start_date=date.today() + relativedelta(months=index),
                end_date=date.today() + relativedelta(
                    months=index + 1, days=-1
                ),
                price=100 - index * 20
            )
            price_tag.save()
            price_tags.append(price_tag)

        # Check price rates tags
        response = self.client.get(
            reverse(
                "listings:api_listing_price_tags",
                kwargs={
                    Listing.Field.slug: self.good_listing_object.slug
                }
            ),
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            len(response.data.get("results")),
            5
        )

        for index in range(5):
            current_tag = response.data.get("results")[index]
            self.assertEqual(
                current_tag.get(PriceTag.Field.start_date),
                price_tags[index].start_date.strftime("%Y-%m-%d")
            )
            self.assertEqual(
                current_tag.get(PriceTag.Field.end_date),
                price_tags[index].end_date.strftime("%Y-%m-%d")
            )
            self.assertEqual(
                float(current_tag.get(PriceTag.Field.price)),
                price_tags[index].price.amount
            )

    def test_get_listing_daily_rates(self) -> None:
        # Append price tags
        price_tag = PriceTag.objects.create(
            listing=self.good_listing_object,
            start_date=date.today(),
            end_date=date.today() + relativedelta(days=6),
            price=100.0
        )
        price_tag.save()

        # Check daily rates
        response = self.client.get(
            reverse(
                "listings:api_listing_daily_rates",
                kwargs={
                    Listing.Field.slug: self.good_listing_object.slug
                }
            ),
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            len(response.data.get("results")),
            7
        )

        for index in range(7):
            current_rate = response.data.get("results")[index]
            self.assertEqual(
                current_rate.get(DayRate.Field.date),
                (date.today() + relativedelta(days=index)).strftime("%Y-%m-%d")
            )
            self.assertEqual(
                float(current_rate.get(DayRate.Field.price)),
                100.0
            )
