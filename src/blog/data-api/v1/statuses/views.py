from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)

from ....models import Status
from .permissions import StatusPermissions
from .serializers import StatusSerializer


class Statuses(ListCreateAPIView):
    """
    Manages statuses listing and new statuses creation
    """

    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [StatusPermissions]


class StatusDetails(RetrieveUpdateDestroyAPIView):
    """
    Manages single status instance lifecycle
    """

    queryset = Status.objects.all()
    lookup_field = Status.Field.name
    lookup_url_kwarg = Status.Field.name
    serializer_class = StatusSerializer
    permission_classes = [StatusPermissions]
