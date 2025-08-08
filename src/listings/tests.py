from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify

from .models import (
    ObjectType, Category, Amenity, HouseRule, Listing
)

good_listing = {
    Listing.Field.title: "First listing",
    Listing.Field.description: "First test listing",
    Listing.Field.max_guests: 2,
    Listing.Field.beds: 1,
    Listing.Field.bedrooms: 1,
    Listing.Field.bathrooms: 1,
    Listing.Field.instant_booking: True
}


class ListingTests(TestCase):
    """
    Testing single listing object lifecycle
    """

    def setUp(self) -> None:
        """
        Prepare test data
        :return:
        """

        # Object type
        self.apartments = ObjectType.objects.create(
            name="Apartments",
            description="Comfortable and with fait price"
        )

        # Amenities (essential and not)
        essentials = Category.objects.create(
            name="Essentials",
            description="Mandatory for everyone"
        )
        perks = Category.objects.create(
            name="Perks",
            description="Non-mandatory goodies"
        )
        electricity = Amenity.objects.create(
            name="Electricity",
            description="For light and appliances",
            category=essentials
        )
        water = Amenity.objects.create(
            name="Water",
            description="For drinking and washing",
            category=essentials
        )
        heating = Amenity.objects.create(
            name="Central heating",
            description="Only for cold countries",
            category=perks
        )
        cooler = Amenity.objects.create(
            name="Cooler",
            description="Only for hot countries",
            category=perks
        )
        self.amenities = [
            electricity,
            water,
            heating,
            cooler
        ]

        # House rules
        no_smoking = HouseRule.objects.create(
            name="No smoking",
            description="Healthy lifestyle preferred",
        )
        pets_allowed = HouseRule.objects.create(
            name="Pets allowed",
            description="Pets are our family members",
        )
        self.house_rules = [
            no_smoking,
            pets_allowed
        ]

        # Create test listing
        self.listing = Listing.objects.create(
            **good_listing,
            slug=slugify(
                good_listing.get(
                    Listing.Field.title
                )
            ),
            object_type=self.apartments
        )
        self.listing.amenities.set(
            self.amenities
        )
        self.listing.house_rules.set(
            self.house_rules
        )

    def test_listings_list(self) -> None:
        # Checking listings list URL and template
        response = self.client.get(reverse("listings:list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "listings/list.html")
        self.assertContains(response, "First listing")

    def test_unknown_listing_details(self) -> None:
        # Checking for non-existing listing details
        no_response = self.client.get("/listing/wrong")
        self.assertEqual(no_response.status_code, 404)

    def test_existing_post_details(self) -> None:
        # Checking existing listing details
        response = self.client.get(self.listing.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "listings/details.html")

        # Checking if all the data available
        self.assertContains(response, self.apartments.name)
        for key in good_listing:
            self.assertContains(
                response,
                good_listing.get(key)
            )
        for amenity in self.amenities:
            self.assertContains(
                response,
                amenity.name
            )
        for rule in self.house_rules:
            self.assertContains(
                response,
                rule.name
            )
