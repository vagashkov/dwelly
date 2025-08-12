from rest_framework.serializers import (
    ModelSerializer, SerializerMethodField
)

from ...models import Listing, Photo


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

    photos = SerializerMethodField("get_photos")

    def get_photos(self, obj: Listing) -> list:
        photos: list = []
        # Get all photos for this listing
        for photo in Photo.objects.filter(
                listing=obj.id
        ).order_by(
            Photo.SORT_KEY
        ):
            photo_description: dict = dict()
            photo_description[Photo.Field.title]: str = photo.title
            photo_description[Photo.Field.index]: int = photo.index
            photo_description[Photo.Field.is_cover]: bool = photo.is_cover
            photo_description["preview"]: str = photo.get_preview()
            photo_description["details"]: str = photo.get_details()

            photos.append(photo_description)
        return photos

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
            "photos"
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
