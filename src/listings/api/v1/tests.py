from os import mkdir
from os.path import exists
from shutil import rmtree

from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import reverse
from django.test import override_settings

from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_403_FORBIDDEN,
    HTTP_422_UNPROCESSABLE_ENTITY
)

from core.api.tests import BaseAPITest
from tests.data import good_listing, TEST_DIR
from tests.objects import create_good_listing

from ...constants import ERROR_KEY
from ...models import (
    ObjectType, Category, Amenity, Listing, Photo
)


class BaseListingsAPITest(BaseAPITest):
    """
    Base class for listings and photos endpoint testing
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

    def tearDown(self) -> None:
        # Cleaning temporary data
        try:
            rmtree(TEST_DIR)
        except OSError:
            pass


@override_settings(MEDIA_ROOT=TEST_DIR)
class ListingsAPITest(BaseListingsAPITest):
    """
    Base class for listings and related entities testing
    """

    def test_create_listing_no_auth(self) -> None:
        # Create new listing without authentication
        response = self.client.post(
            reverse("listings:api_list"),
            good_listing,
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_create_listing_standard_user(self) -> None:
        # Create new listing as standard user
        self.engage_user()

        response = self.client.post(
            reverse("listings:api_list"),
            good_listing,
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_create_listing_no_object_type(self) -> None:
        # Create new listing as admin
        self.engage_admin()

        data = good_listing.copy()

        response = self.client.post(
            reverse("listings:api_list"),
            data,
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_422_UNPROCESSABLE_ENTITY
        )

    def test_create_listing_zero_guests(self) -> None:
        # Create new listing as admin
        self.engage_admin()

        data = good_listing.copy()
        data[Listing.Field.max_guests] = 0

        response = self.client.post(
            reverse("listings:api_list"),
            data,
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_422_UNPROCESSABLE_ENTITY
        )

        self.assertIn(
            Listing.Field.max_guests,
            response.data.get(
                ERROR_KEY
            )
        )

    def test_create_listing_zero_bedrooms(self) -> None:
        # Create new listing as admin
        self.engage_admin()

        data = good_listing.copy()
        data[Listing.Field.bedrooms] = 0

        response = self.client.post(
            reverse("listings:api_list"),
            data,
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_422_UNPROCESSABLE_ENTITY
        )

        self.assertIn(
            Listing.Field.bedrooms,
            response.data.get(
                ERROR_KEY
            )
        )

    def test_create_listing_zero_beds(self) -> None:
        # Create new listing as admin
        self.engage_admin()

        data = good_listing.copy()
        data[Listing.Field.beds] = -2

        response = self.client.post(
            reverse("listings:api_list"),
            data,
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_422_UNPROCESSABLE_ENTITY
        )

        self.assertIn(
            Listing.Field.beds,
            response.data.get(
                ERROR_KEY
            )
        )

    def test_create_listing_zero_bathrooms(self) -> None:
        # Create new listing as admin
        self.engage_admin()

        data = good_listing.copy()
        data[Listing.Field.bathrooms] = -3

        response = self.client.post(
            reverse("listings:api_list"),
            data,
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_422_UNPROCESSABLE_ENTITY
        )

        self.assertIn(
            Listing.Field.bathrooms,
            response.data.get(
                ERROR_KEY
            )
        )

    def test_create_listing_wrong_amenities(self) -> None:
        # Create new listing as admin
        self.engage_admin()

        data = good_listing.copy()
        bad_amenities = [-1, 999]
        data[Listing.Field.amenities] = bad_amenities

        response = self.client.post(
            reverse("listings:api_list"),
            data,
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_422_UNPROCESSABLE_ENTITY
        )

        for amenity in bad_amenities:
            self.assertIn(
                str(amenity),
                "".join(
                    response.data.get(
                        ERROR_KEY
                    ).get(
                        Listing.Field.amenities
                    )
                )
            )

    def test_create_listing_wrong_house_rules(self) -> None:
        # Create new listing as admin
        self.engage_admin()

        data = good_listing.copy()
        bad_rules = [-1, 999]
        data[Listing.Field.house_rules] = bad_rules

        response = self.client.post(
            reverse("listings:api_list"),
            data,
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_422_UNPROCESSABLE_ENTITY
        )

        for rule in bad_rules:
            self.assertIn(
                str(rule),
                "".join(
                    response.data.get(
                        ERROR_KEY
                    ).get(
                        Listing.Field.house_rules
                    )
                )
            )

    def test_create_listing(self) -> None:
        # Create new listing as admin
        self.engage_admin()

        data = good_listing.copy()
        data[Listing.Field.object_type] = ObjectType.objects.create(
            name="House"
        ).id
        data[Listing.Field.house_rules] = []
        data[Listing.Field.amenities] = [
            Amenity.objects.create(
                name="Windows",
                category=Category.objects.create(name="Essentials")
            ).id
        ]

        response = self.client.post(
            reverse("listings:api_list"),
            data,
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_201_CREATED
        )

    def test_listings_list(self) -> None:
        listing_object = create_good_listing()

        # Checking listings list URL and template
        response = self.client.get(reverse("listings:api_list"))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            len(response.data["results"]),
            1
        )
        listing_description = response.data.get("results")[0]
        self.assertEqual(
            listing_description.get(Listing.Field.title),
            listing_object.title
        )
        self.assertEqual(
            listing_description.get(Listing.Field.object_type),
            listing_object.object_type.id
        )
        self.assertEqual(
            listing_description.get(Listing.Field.slug),
            listing_object.slug
        )
        self.assertEqual(
            listing_description.get(Listing.Field.cover_photo),
            listing_object.get_cover_photo().get_preview()
        )

    def test_listing_details(self) -> None:
        listing_object = create_good_listing()

        # Checking listings list URL and template
        response = self.client.get(
            reverse(
                "listings:api_listing_details",
                kwargs={
                    Listing.Field.slug: listing_object.slug
                }
            ),
        )
        self.assertEqual(response.status_code, 200)

        for key in good_listing.keys():
            self.assertEqual(
                response.data.get(key),
                good_listing.get(key)
            )
        for amenity in listing_object.amenities.all():
            self.assertIn(
                amenity.id,
                response.data.get(Listing.Field.amenities)
            )
        for rule in listing_object.house_rules.all():
            self.assertIn(
                rule.id,
                response.data.get(Listing.Field.house_rules)
            )
        # Now check photos
        photo_object = Photo.objects.get(
            listing=listing_object,
            index=0
        )
        self.assertIn(
            "photos",
            response.data
        )
        self.assertEqual(
            len(response.data.get("photos")),
            1
        )
        self.assertEqual(
            response.data.get("photos")[0].get(Photo.Field.title),
            photo_object.title
        )
        self.assertEqual(
            response.data.get("photos")[0].get("preview"),
            photo_object.get_preview()
        )
        self.assertEqual(
            response.data.get("photos")[0].get("details"),
            photo_object.get_details()
        )
