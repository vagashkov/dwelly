from rest_framework.serializers import ModelSerializer

from core.models import Reference

from .....models import Category


class CategorySerializer(ModelSerializer):
    """
    Manages Category objects serialization
    """

    class Meta:
        model = Category
        fields = [
            Reference.Field.name,
            Reference.Field.description,
            ]
