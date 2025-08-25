from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)

from .....models import ReservationStatus
from .permissions import ReservationStatusPermissions
from .serializers import ReservationStatusSerializer


class Statuses(ListCreateAPIView):
    """
    Manages reservation statuses listing and new statuses creation
    """

    queryset = ReservationStatus.objects.all()
    serializer_class = ReservationStatusSerializer
    pagination_class = None
    permission_classes = [ReservationStatusPermissions]


class StatusDetails(RetrieveUpdateDestroyAPIView):
    """
    Manages single reservation status instance lifecycle
    """

    queryset = ReservationStatus.objects.all()
    lookup_field = ReservationStatus.Field.name
    lookup_url_kwarg = ReservationStatus.Field.name
    serializer_class = ReservationStatusSerializer
    permission_classes = [ReservationStatusPermissions]
