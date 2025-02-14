from pydantic import ValidationError
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from ....constants import (
    ERROR_MSG_NO_INITIAL_STATUS,
)
from ....models import Post, Status
from .permissions import PostPermissions
from .serializers import (
    GetListSerializer,
    GetDetailsSerializer,
    PostSerializer
)
from .validators import PostValidator


class Posts(ListCreateAPIView):
    """
    Manages posts listing and new post creation
    """

    queryset = Post.objects.all()
    serializer_class = GetListSerializer
    permission_classes = [PostPermissions]

    def post(self, request, *args, **kwargs):
        """
        Blog post creation routine
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        # First, validate data using pydantic class
        try:
            PostValidator.parse_obj(request.data)
        except ValidationError as error:
            return Response(
                status=HTTP_422_UNPROCESSABLE_ENTITY,
                # Leave only first error message for every field
                data={
                    "errors": error.errors()
                }
            )

        # Deserialize and check data
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Obtain initial status
        try:
            initial_status = Status.objects.get(
                is_initial=True
                )
        except Status.DoesNotExist:
            return Response(
                status=HTTP_422_UNPROCESSABLE_ENTITY,
                # Leave only first error message for every field
                data={
                    "errors": ERROR_MSG_NO_INITIAL_STATUS
                }
            )

        # Try to create post object
        post = serializer.save(
            author=request.user,
            status=initial_status
        )
        headers = self.get_success_headers(serializer.data)

        post_data = GetDetailsSerializer(post).data
        post_data[Post.Field.slug] = post.slug
        post_data[Post.Field.status] = post.status.name

        # And return result
        return Response(
            post_data,
            status=HTTP_201_CREATED,
            headers=headers
        )


class PostDetails(RetrieveUpdateDestroyAPIView):
    """
    Manages single post instance lifecycle
    """

    queryset = Post.objects.all()
    lookup_field = Post.Field.slug
    lookup_url_kwarg = Post.Field.slug
    serializer_class = GetDetailsSerializer
    permission_classes = [PostPermissions]
