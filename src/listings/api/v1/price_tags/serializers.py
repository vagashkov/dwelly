from rest_framework.serializers import ModelSerializer

from ....models import PriceTag


class PriceTagSerializer(ModelSerializer):
    """
    Manages PriceTag objects serialization
    """

    class Meta:
        model = PriceTag
        fields = [
            PriceTag.Field.start_date,
            PriceTag.Field.end_date,
            PriceTag.Field.price,
            PriceTag.Field.description
            ]
