from os import mkdir
from os.path import exists
from shutil import rmtree

from PIL import Image

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils.text import slugify

from .models import (
    ObjectType, Category, Amenity, HouseRule,
    Listing, Photo
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

TEST_DIR = settings.BASE_DIR / "test_data"


class ListingTests(TestCase):
    """
    Testing single listing object lifecycle
    """

    def upload_cover(self, listing: Listing) -> None:
        # prepare test image to upload
        image = Image.new(
            "RGB",
            size=(2000, 2000),
            color=(155, 0, 0)
        )

        if not exists(TEST_DIR):
            mkdir(TEST_DIR)

        image_path = TEST_DIR / "test_photo.jpg"
        image.save(image_path)

        cover_photo = Photo(
            index=0,
            title="Test cover photo",
            listing=listing,
            is_cover=True
        )

        # "upload" post cover
        with open(image_path, "rb") as profile_photo:
            cover_photo.file = SimpleUploadedFile(
                name="post_cover.jpg",
                content=profile_photo.read(),
                content_type="image/jpeg"
            )

        cover_photo.save()

    @override_settings(MEDIA_ROOT=TEST_DIR)
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
        self.listing.save()

        self.upload_cover(self.listing)

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

        self.assertContains(
            response,
            self.listing.get_cover_photo().get_details()
        )
