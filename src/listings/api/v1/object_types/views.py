from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)

from core.models import Reference

from ....models import ObjectType
from .permissions import ObjectTypePermissions
from .serializers import ObjectTypeSerializer


class ObjectTypes(ListCreateAPIView):
    """
    Manages object types listing and new object types creation
    """

    queryset = ObjectType.objects.all()
    serializer_class = ObjectTypeSerializer
    pagination_class = None
    permission_classes = [ObjectTypePermissions]


class ObjectTypeDetails(RetrieveUpdateDestroyAPIView):
    """
    Manages single object type instance lifecycle
    """

    queryset = ObjectType.objects.all()
    lookup_field = Reference.Field.name
    lookup_url_kwarg = Reference.Field.name
    serializer_class = ObjectTypeSerializer
    permission_classes = [ObjectTypePermissions]
