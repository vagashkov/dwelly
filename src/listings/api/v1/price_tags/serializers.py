from rest_framework.serializers import ModelSerializer

from ....models import PriceTag, DayRate


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


class DayRateSerializer(ModelSerializer):
    """
    Manages DayRate objects serialization
    """

    class Meta:
        model = DayRate
        fields = [
            DayRate.Field.listing,
            DayRate.Field.price_tag,
            DayRate.Field.date,
            DayRate.Field.price,
            DayRate.Field.description
            ]
