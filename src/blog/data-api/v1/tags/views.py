from rest_framework.generics import ListCreateAPIView

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
