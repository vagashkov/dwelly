from rest_framework.serializers import ModelSerializer

from ....models import Reservation


class ReservationSerializer(ModelSerializer):
    """
    Manages PriceTag objects serialization
    """

    class Meta:
        model = Reservation
        fields = [
            Reservation.Field.check_in,
            Reservation.Field.check_out,
            Reservation.Field.comment
            ]
        read_only_fields = (
            Reservation.Field.user,
        )
