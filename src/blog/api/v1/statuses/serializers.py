from rest_framework.serializers import ModelSerializer

from ....models import Status


class StatusSerializer(ModelSerializer):
    """
    Manages Status objects serialization
    """

    class Meta:
        model = Status
        fields = [
            Status.Field.name,
            Status.Field.description,
            Status.Field.is_initial
            ]
