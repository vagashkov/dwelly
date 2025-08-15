from rest_framework.serializers import ModelSerializer

from core.models import Reference

from ....models import ObjectType


class ObjectTypeSerializer(ModelSerializer):
    """
    Manages ObjectType objects serialization
    """

    class Meta:
        model = ObjectType
        fields = [
            Reference.Field.name,
            Reference.Field.description,
            ]
