from rest_framework.serializers import (
    ModelSerializer, SerializerMethodField
)

from ....models import Reservation


class ReservationSerializer(ModelSerializer):
    """
    Manages PriceTag objects serialization
    """

    cost = SerializerMethodField()

    def get_cost(self, instance):
        return instance.cost.amount

    currency = SerializerMethodField()

    def get_currency(self, instance):
        return instance.cost.currency.code

    class Meta:
        model = Reservation
        fields = [
            Reservation.Field.check_in,
            Reservation.Field.check_out,
            Reservation.Field.comment,
            Reservation.Field.cost,
            Reservation.Field.currency
            ]
        read_only_fields = (
            Reservation.Field.user,
            Reservation.Field.cost,
            Reservation.Field.currency
        )
