from rest_framework.serializers import ModelSerializer

from ...models import Listing


class GetListingDigest(ModelSerializer):
    """
    Manages listing objects serialization
    """

    # cover_photo = SerializerMethodField()
    #
    # def get_cover_photo(self, object: Listing) -> str:
    #     if object.get_cover_photo():
    #         return object.get_cover_photo().file.url

    class Meta:
        model = Listing
        fields = [
            Listing.Field.title,
            Listing.Field.object_type,
            Listing.Field.slug,
            # Listing.Field.cover_photo,
            ]


class GetListingDetails(GetListingDigest):
    """
    Manages listing object details serialization
    """

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
