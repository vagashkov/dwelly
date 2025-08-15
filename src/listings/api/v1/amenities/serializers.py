from rest_framework.serializers import ModelSerializer

from core.models import Reference

from ....models import Amenity


class AmenitySerializer(ModelSerializer):
    """
    Manages Amenity objects serialization
    """

    class Meta:
        model = Amenity
        fields = [
            Reference.Field.name,
            Reference.Field.description,
            Amenity.Field.category
            ]
