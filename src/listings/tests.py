from datetime import date
from dateutil.relativedelta import relativedelta
from shutil import rmtree

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from core.models import Reference
from tests.objects import (
    object_type, amenities_list, house_rules_list,
    good_listing, create_good_listing, TEST_DIR
)

from .models import PriceTag, DayRate, Reservation


class ListingTests(TestCase):
    """
    Testing single listing object lifecycle
    """

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def setUp(self) -> None:
        """
        Prepare test data
        :return:
        """

        self.listing = create_good_listing()

    def tearDown(self) -> None:
        # Cleaning temporary data
        try:
            rmtree(TEST_DIR)
        except OSError:
            pass

    def test_listings_list(self) -> None:
        # Checking listings list URL and template
        response = self.client.get(reverse("listings:list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "listings/list.html")
        self.assertContains(response, self.listing.title)
        self.assertContains(response, self.listing.object_type.name)
        self.assertContains(
            response,
            self.listing.get_cover_photo().get_preview()
        )

    def test_unknown_listing_details(self) -> None:
        # Checking for non-existing listing details
        no_response = self.client.get("/listing/wrong")
        self.assertEqual(no_response.status_code, 404)

    def test_existing_listing_details(self) -> None:
        # Checking existing listing details
        response = self.client.get(self.listing.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "listings/details.html")

        # Checking if all the data available
        self.assertContains(response, object_type.get(Reference.Field.name))
        for key in good_listing:
            self.assertContains(
                response,
                good_listing.get(key)
            )
        for amenity in amenities_list:
            self.assertContains(
                response,
                amenity.get(Reference.Field.name)
            )
        for rule in house_rules_list:
            self.assertContains(
                response,
                rule.get(Reference.Field.name)
            )
        for price_tag in self.listing.price_tags.all():
            self.assertContains(
                response,
                price_tag
            )

        self.assertContains(
            response,
            self.listing.get_cover_photo().get_details()
        )

    def test_reservation_form_anonymous_user(self) -> None:
        # Checking existing listing details
        response = self.client.get(self.listing.get_absolute_url())
        self.assertContains(
            response,
            "to view available dates and submit for reservation "
        )

    def test_reservation_form_registered_user(self) -> None:
        user = get_user_model().objects.create_user(
            email="user@test.com",
            password="VeryStr0ngPwd"
        )
        self.client.force_login(user)

        # Checking existing listing details
        response = self.client.get(self.listing.get_absolute_url())
        self.assertContains(
            response,
            "Submit for reservation"
        )

    def test_reservation_overlapping_dates(self) -> None:
        user = get_user_model().objects.create_user(
            email="user@test.com",
            password="VeryStr0ngPwd"
        )
        self.client.force_login(user)
        Reservation.objects.create(
            listing=self.listing,
            check_in=date.today(),
            check_out=date.today() + relativedelta(days=7),
            user=user
        ).save()
        # with self.assertRaises(ValidationError):
        response = self.client.post(
            self.listing.get_absolute_url(),
            {
                "listing": self.listing.slug,
                "check_in": date.today() + relativedelta(days=1),
                "check_out": date.today() + relativedelta(days=6)
            }
        )
        self.assertContains(
            response,
            "Some overlapping dates were found"
        )

    def test_day_rates_created(self) -> None:
        """

        :return:
        """
        # Append price tags
        for index in range(5):
            price_tag = PriceTag.objects.create(
                listing=self.listing,
                start_date=date.today() + relativedelta(months=index),
                end_date=date.today() + relativedelta(
                    months=index + 1, days=-1
                ),
                price=100 - index * 20
            )
            price_tag.save()

            day_rate = DayRate.objects.get(
                listing=self.listing,
                price_tag=price_tag,
                date=date.today() + relativedelta(months=index)
            )
            self.assertEqual(
                day_rate.price.amount,
                100-index*20
            )
