from rest_framework.serializers import ModelSerializer

from .....models import ReservationStatus


class ReservationStatusSerializer(ModelSerializer):
    """
    Manages ReservationStatus objects serialization
    """

    class Meta:
        model = ReservationStatus
        fields = [
            ReservationStatus.Field.name,
            ReservationStatus.Field.description,
            ReservationStatus.Field.is_initial
            ]
