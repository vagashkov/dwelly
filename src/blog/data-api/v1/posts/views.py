from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
)

from ....models import Post
from .permissions import PostPermissions
from .serializers import (
    GetListSerializer, GetDetailsSerializer
)


class Posts(ListCreateAPIView):
    """
    Manages posts listing and new post creation
    """

    queryset = Post.objects.all()
    serializer_class = GetListSerializer
    permission_classes = [PostPermissions]


class PostDetails(RetrieveUpdateDestroyAPIView):
    """
    Manages single post instance lifecycle
    """

    queryset = Post.objects.all()
    lookup_field = Post.Field.slug
    lookup_url_kwarg = Post.Field.slug
    serializer_class = GetDetailsSerializer
    permission_classes = [PostPermissions]
