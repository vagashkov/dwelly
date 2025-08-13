import io
from PIL import Image

from django.shortcuts import reverse
from django.test import override_settings

from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_403_FORBIDDEN,
    HTTP_422_UNPROCESSABLE_ENTITY
)

from ..tests import BaseListingsAPITest, TEST_DIR

from ....models import Listing, Photo

from .constants import (
    ERROR_KEY, ERROR_MSG_NO_PHOTO_ATTACHED,
    ERROR_MSG_NO_PHOTO_INDEX,
    ERROR_MSG_NO_PHOTO_TITLE,
    ERROR_MSG_UNKNOWN_LISTING
)


def make_good_photo() -> dict:
    """

    :return:
    """
    file = io.BytesIO()
    image = Image.new("RGB", size=(2000, 2000), color=(155, 0, 0))
    image.save(file, "JPEG")
    file.name = "test.jpeg"
    file.seek(0)

    return {
        Photo.Field.file: file,
        Photo.Field.title: "Main view",
        Photo.Field.index: 1,
        Photo.Field.is_cover: True
        }


class Photos(BaseListingsAPITest):
    """
    Test listing photo lifecycle endpoints
    """

    def setUp(self) -> None:
        """

        :return:
        """
        self.good_listing_object = self.create_good_listing()

    def test_create_photo_no_auth(self) -> None:

        # Create new listing photo without authentication
        response = self.client.post(
            reverse(
                "listings:api_listing_photos",
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

    def test_create_photo_standard_user(self) -> None:
        # Working as a standard (non-admin) user
        self.engage_user()

        # Create new listing photo
        response = self.client.post(
            reverse(
                "listings:api_listing_photos",
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

    def test_create_photo_no_file(self) -> None:
        # Working as an admin
        self.engage_admin()

        data = make_good_photo()
        del data[Photo.Field.file]

        # Create new listing photo
        response = self.client.post(
            reverse(
                "listings:api_listing_photos",
                kwargs={
                    Listing.Field.slug:
                        self.good_listing_object.slug
                }
            ),
            data,
            format="multipart"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_422_UNPROCESSABLE_ENTITY
        )

        self.assertEqual(
             response.data.get(ERROR_KEY),
             ERROR_MSG_NO_PHOTO_ATTACHED
        )

    def test_create_photo_no_title(self) -> None:
        # Working as an admin
        self.engage_admin()

        data = make_good_photo()
        del data[Photo.Field.title]

        # Create new listing photo
        response = self.client.post(
            reverse(
                "listings:api_listing_photos",
                kwargs={
                    Listing.Field.slug:
                        self.good_listing_object.slug
                }
            ),
            data,
            format="multipart"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_422_UNPROCESSABLE_ENTITY
        )

        self.assertEqual(
             response.data.get(ERROR_KEY),
             ERROR_MSG_NO_PHOTO_TITLE
        )

    def test_create_photo_no_index(self) -> None:
        # Working as an admin
        self.engage_admin()

        data = make_good_photo()
        del data[Photo.Field.index]

        # Create new listing photo
        response = self.client.post(
            reverse(
                "listings:api_listing_photos",
                kwargs={
                    Listing.Field.slug:
                        self.good_listing_object.slug
                }
            ),
            data,
            format="multipart"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_422_UNPROCESSABLE_ENTITY
        )

        self.assertEqual(
             response.data.get(ERROR_KEY),
             ERROR_MSG_NO_PHOTO_INDEX
        )

    def test_create_photo_unknown_listing(self) -> None:
        # Working as an admin
        self.engage_admin()

        # Create new listing photo
        response = self.client.post(
            reverse(
                "listings:api_listing_photos",
                kwargs={
                    Listing.Field.slug: "000000"
                }
            ),
            make_good_photo(),
            format="multipart"
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

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def test_create_photo(self) -> None:
        # Working as an admin
        self.engage_admin()

        data = make_good_photo()

        # Create new listing photo
        response = self.client.post(
            reverse(
                "listings:api_listing_photos",
                kwargs={
                    Listing.Field.slug:
                        self.good_listing_object.slug
                }
            ),
            data,
            format="multipart"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_201_CREATED
        )

        self.assertEqual(
              response.data.get(Photo.Field.title),
              data.get(Photo.Field.title)
        )
        self.assertEqual(
            response.data.get(Photo.Field.index),
            data.get(Photo.Field.index)
        )
        self.assertEqual(
            response.data.get(Photo.Field.is_cover),
            data.get(Photo.Field.is_cover)
        )
        self.assertIn(
            "preview",
            response.data,
        )
        self.assertIn(
            "details",
            response.data,
        )
