from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)

from core.models import Reference

from .....models import Category
from .permissions import CategoryPermissions
from .serializers import CategorySerializer


class Categories(ListCreateAPIView):
    """
    Manages categories listing and new categories creation
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None
    permission_classes = [CategoryPermissions]


class CategoryDetails(RetrieveUpdateDestroyAPIView):
    """
    Manages single category instance lifecycle
    """

    queryset = Category.objects.all()
    lookup_field = Reference.Field.name
    lookup_url_kwarg = Reference.Field.name
    serializer_class = CategorySerializer
    permission_classes = [CategoryPermissions]
