from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)

from core.models import Reference

from ....models import Amenity
from .permissions import AmenityPermissions
from .serializers import AmenitySerializer


class Amenities(ListCreateAPIView):
    """
    Manages statuses listing and new amenities creation
    """

    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
    pagination_class = None
    permission_classes = [AmenityPermissions]


class AmenityDetails(RetrieveUpdateDestroyAPIView):
    """
    Manages single amenity instance lifecycle
    """

    queryset = Amenity.objects.all()
    lookup_field = Reference.Field.name
    lookup_url_kwarg = Reference.Field.name
    serializer_class = AmenitySerializer
    permission_classes = [AmenityPermissions]
