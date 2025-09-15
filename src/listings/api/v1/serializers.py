from rest_framework.serializers import (
    ModelSerializer, TimeField, SerializerMethodField
)

from .photos.serializers import PhotoSerializer
from .price_tags.serializers import PriceTagSerializer

from ...models import Listing


class GetListingDigest(ModelSerializer):
    """
    Manages listing objects serialization
    """

    cover_photo = SerializerMethodField()

    def get_cover_photo(self, object: Listing) -> str:
        if object.get_cover_photo():
            return object.get_cover_photo().get_preview()

    class Meta:
        model = Listing
        fields = [
            Listing.Field.title,
            Listing.Field.object_type,
            Listing.Field.slug,
            Listing.Field.cover_photo,
            ]


class GetListingDetails(GetListingDigest):
    """
    Manages listing object details serialization
    """

    check_in_time: TimeField = TimeField(format="%H:%M")
    check_out_time: TimeField = TimeField(format="%H:%M")

    photos = SerializerMethodField("get_photos")

    def get_photos(self, obj: Listing) -> list:
        return PhotoSerializer(
            obj.get_photos(),
            many=True
        ).data

    price_tags = SerializerMethodField("get_price_tags")

    def get_price_tags(self, obj: Listing) -> list:
        return PriceTagSerializer(
            obj.get_price_tags(),
            many=True
        ).data

    class Meta:
        model = Listing
        fields = [
            # Base info
            Listing.Field.object_type,
            Listing.Field.title,
            Listing.Field.description,
            # Capacity
            Listing.Field.max_guests,
            Listing.Field.bedrooms,
            Listing.Field.beds,
            Listing.Field.bathrooms,
            # Add-ons
            Listing.Field.amenities,
            Listing.Field.house_rules,
            # Reservation
            Listing.Field.check_in_time,
            Listing.Field.check_out_time,
            Listing.Field.instant_booking,
            # Other info
            "photos",
            "price_tags"
            ]


class PostListingSerializer(ModelSerializer):
    """
    Manages listing object initial creation
    """

    class Meta:
        """
        """
        model = Listing
        fields = [
            # Base info
            Listing.Field.object_type,
            Listing.Field.title,
            Listing.Field.slug,
            Listing.Field.description,
            # Capacity
            Listing.Field.max_guests,
            Listing.Field.bedrooms,
            Listing.Field.beds,
            Listing.Field.bathrooms,
            # Add-ons
            Listing.Field.amenities,
            Listing.Field.house_rules,
            # Reservation
            Listing.Field.check_in_time,
            Listing.Field.check_out_time,
            Listing.Field.instant_booking,
            ]
