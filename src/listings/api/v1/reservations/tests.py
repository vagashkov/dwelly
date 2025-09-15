from datetime import date
from dateutil.relativedelta import relativedelta

from django.conf import settings
from django.shortcuts import reverse

from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_403_FORBIDDEN,
    HTTP_422_UNPROCESSABLE_ENTITY
)

from tests.data import good_reservation
from tests.objects import create_good_listing

from ....models import Listing, PriceTag, Reservation

from ..constants import (
    ERROR_KEY, ERROR_MSG_UNKNOWN_LISTING
)
from ..tests import BaseListingsAPITest


required_fields = [
    Reservation.Field.check_in,
    Reservation.Field.check_out
]


class Reservations(BaseListingsAPITest):
    """
    Test listing reservation lifecycle endpoints
    """

    def setUp(self) -> None:
        """

        :return:
        """
        self.listing = create_good_listing()

        PriceTag.objects.create(
            listing=self.listing,
            start_date=date.today(),
            end_date=date.today() + relativedelta(weeks=5),
            price=100
        ).save()

    def test_create_reservation_no_auth(self) -> None:
        # Create new listing reservation without authentication
        response = self.client.post(
            reverse(
                "listings:api_listing_reservations",
                kwargs={
                    Listing.Field.slug:
                        self.listing.slug
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

    def test_create_reservation_no_required_field(self) -> None:
        # Working as an admin
        self.engage_user()

        for key in required_fields:
            data = good_reservation.copy()
            del data[key]

            # Create new listing price tag
            response = self.client.post(
                reverse(
                    "listings:api_listing_reservations",
                    kwargs={
                        Listing.Field.slug:
                        self.listing.slug
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

    def test_create_reservation_unknown_listing(self) -> None:
        # Working as user
        self.engage_user()

        # Create new listing price tag
        response = self.client.post(
            reverse(
                "listings:api_listing_reservations",
                kwargs={
                    Listing.Field.slug: "000000"
                }
            ),
            good_reservation,
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

    def test_create_reservation(self) -> None:
        # Working as an admin
        self.engage_user()

        # Create new listing reservation
        response = self.client.post(
            reverse(
                "listings:api_listing_reservations",
                kwargs={
                    Listing.Field.slug:
                        self.listing.slug
                }
            ),
            good_reservation,
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_201_CREATED
        )

        self.assertEqual(
            response.data.get(Reservation.Field.check_in),
            good_reservation.get(
                Reservation.Field.check_in
            ).strftime("%Y-%m-%d")
        )
        self.assertEqual(
            response.data.get(Reservation.Field.check_out),
            good_reservation.get(
                Reservation.Field.check_out
            ).strftime("%Y-%m-%d")
        )
        self.assertEqual(
            response.data.get(Reservation.Field.comment),
            good_reservation.get(Reservation.Field.comment)
        )

    def test_get_listing_reservations(self) -> None:
        user = self.engage_user()

        # Append reservations
        reservations = list()
        for index in range(5):
            reservation = Reservation.objects.create(
                listing=self.listing,
                user=user,
                check_in=date.today() + relativedelta(weeks=index),
                check_out=date.today() + relativedelta(
                    weeks=index + 1, days=-1
                ),
            )
            reservation.save()
            reservations.append(reservation)

        # Check reservations
        response = self.client.get(
            reverse(
                "listings:api_listing_reservations",
                kwargs={
                    Listing.Field.slug: self.listing.slug
                }
            ),
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            len(response.data.get("results")),
            5
        )

        for index in range(5):
            current_reservation = response.data.get("results")[index]
            self.assertEqual(
                current_reservation.get(Reservation.Field.check_in),
                reservations[index].check_in.strftime("%Y-%m-%d")
            )
            self.assertEqual(
                current_reservation.get(Reservation.Field.check_out),
                reservations[index].check_out.strftime("%Y-%m-%d")
            )
            self.assertIn(
                Reservation.Field.cost,
                current_reservation
            )
            self.assertEqual(
                settings.BASE_CURRENCY,
                current_reservation.get(
                    Reservation.Field.currency
                    )
            )
