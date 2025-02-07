from rest_framework.serializers import (
    ModelSerializer,
)

from ....models import Tag


class TagSerializer(ModelSerializer):
    """
    Manages Category objects serialization
    """

    class Meta:
        model = Tag
        fields = [
            Tag.Field.name,
            Tag.Field.description
            ]
