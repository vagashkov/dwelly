from rest_framework.serializers import ModelSerializer

from core.models import Reference

from ....models import HouseRule


class HouseRuleSerializer(ModelSerializer):
    """
    Manages HouseRule objects serialization
    """

    class Meta:
        model = HouseRule
        fields = [
            Reference.Field.name,
            Reference.Field.description,
            ]
