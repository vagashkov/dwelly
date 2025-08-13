from rest_framework.serializers import (
    ModelSerializer, SerializerMethodField
)

from ....models import Photo


class PhotoSerializer(ModelSerializer):
    """
    Manages Photo objects serialization
    """

    preview = SerializerMethodField("get_preview")

    def get_preview(self, photo: Photo) -> str:
        return photo.get_preview()

    details = SerializerMethodField("get_details")

    def get_details(self, photo: Photo) -> str:
        return photo.get_details()

    class Meta:
        model = Photo
        fields = [
            Photo.Field.title,
            Photo.Field.index,
            Photo.Field.is_cover,
            "preview",
            "details"
            ]
