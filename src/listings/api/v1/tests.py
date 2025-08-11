from django.shortcuts import reverse

from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_403_FORBIDDEN,
    HTTP_422_UNPROCESSABLE_ENTITY
)

from core.api.tests import BaseAPITest

from ...constants import ERROR_KEY
from ...models import (
    ObjectType, Category, Amenity, HouseRule,
    Listing
)


class BaseListingsAPITest(BaseAPITest):
    """
    Base class for listings and related entities testing
    """

    @classmethod
    def setUpTestData(cls) -> None:
        cls.apartments = ObjectType.objects.create(name="Apartments")

        essentials = Category.objects.create(name="Essentials")
        hot_water = Amenity.objects.create(
            name="Hot water",
            category=essentials
        )
        conditioning = Amenity.objects.create(
            name="Conditioning",
            category=essentials
        )
        cls.amenities = [hot_water, conditioning]

        no_smoking = HouseRule.objects.create(name="No smoking")
        pets_allowed = HouseRule.objects.create(name="Pets allowed")
        cls.house_rules = [no_smoking, pets_allowed]

        cls.good_listing = {
            Listing.Field.object_type: cls.apartments.id,
            Listing.Field.title: "Test listing",
            Listing.Field.description: "Test listing description",
            Listing.Field.max_guests: 2,
            Listing.Field.bedrooms: 1,
            Listing.Field.beds: 1,
            Listing.Field.bathrooms: 1,
            Listing.Field.amenities: [
                amenity.id for amenity in cls.amenities
            ],
            Listing.Field.house_rules: [
                rule.id for rule in cls.house_rules
            ],
            Listing.Field.check_in_time: "14:00",
            Listing.Field.check_out_time: "12:00",
            Listing.Field.instant_booking: True
        }

    def create_good_listing(self) -> Listing:
        data = self.good_listing.copy()
        del data[Listing.Field.amenities]
        del data[Listing.Field.house_rules]
        data[Listing.Field.object_type] = self.apartments
        return Listing.objects.create(
            **data
        )


class ListingsTest(BaseListingsAPITest):
    """
    Testing listings endpoint
    """

    def test_create_listing_no_auth(self) -> None:
        # Create new listing without authentication
        response = self.client.post(
            reverse("listings:api_listings"),
            self.good_listing,
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
            reverse("listings:api_listings"),
            self.good_listing,
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

        data = self.good_listing.copy()
        del data[Listing.Field.object_type]

        response = self.client.post(
            reverse("listings:api_listings"),
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

        data = self.good_listing.copy()
        data[Listing.Field.max_guests] = 0

        response = self.client.post(
            reverse("listings:api_listings"),
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

        data = self.good_listing.copy()
        data[Listing.Field.bedrooms] = 0

        response = self.client.post(
            reverse("listings:api_listings"),
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

        data = self.good_listing.copy()
        data[Listing.Field.beds] = -2

        response = self.client.post(
            reverse("listings:api_listings"),
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

        data = self.good_listing.copy()
        data[Listing.Field.bathrooms] = -3

        response = self.client.post(
            reverse("listings:api_listings"),
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

        data = self.good_listing.copy()
        bad_amenities = [-1, 999]
        data[Listing.Field.amenities] += bad_amenities

        response = self.client.post(
            reverse("listings:api_listings"),
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

        data = self.good_listing.copy()
        bad_rules = [-1, 999]
        data[Listing.Field.house_rules] += bad_rules

        response = self.client.post(
            reverse("listings:api_listings"),
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

        response = self.client.post(
            reverse("listings:api_listings"),
            self.good_listing,
            format="json"
        )

        # Check results through response code and error message
        self.assertEqual(
            response.status_code,
            HTTP_201_CREATED
        )
