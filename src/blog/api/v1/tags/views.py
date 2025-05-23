from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)

from ....models import Tag
from .permissions import TagPermissions
from .serializers import TagSerializer


class Tags(ListCreateAPIView):
    """
    Manages tag listing and new tags creation
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [TagPermissions]


class TagDetails(RetrieveUpdateDestroyAPIView):
    """
    Manages single tag instance lifecycle
    """

    queryset = Tag.objects.all()
    lookup_field = Tag.Field.name
    lookup_url_kwarg = Tag.Field.name
    serializer_class = TagSerializer
    permission_classes = [TagPermissions]
