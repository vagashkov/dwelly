import PIL
from PIL import Image
from pydantic import ValidationError
from django.db.models import Q
from rest_framework.generics import (
    ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    HTTP_422_UNPROCESSABLE_ENTITY,
)
from rest_framework.views import APIView

from core.models import BaseModel

from ....constants import (
    ERROR_KEY,
    ERROR_MSG_NO_INITIAL_STATUS,
    ERROR_MSG_NO_IMAGE_ATTACHED,
    ERROR_MSG_UNSUPPORTED_IMAGE_FORMAT,
    ERROR_MSG_NO_POST,
    ERROR_MSG_MULTIPLE_POSTS
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

    def post(
            self,
            request: Request,
            *args: list,
            **kwargs: dict
    ) -> Response:
        """
        Blog post creation routine
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        # First, validate data using pydantic class
        try:
            PostValidator.model_validate(
                    request.data
                    )
        except ValidationError as error:
            return Response(
                status=HTTP_422_UNPROCESSABLE_ENTITY,
                data={
                    ERROR_KEY: error.errors()
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
                    ERROR_KEY: ERROR_MSG_NO_INITIAL_STATUS
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


class Search(ListAPIView):
    """
    Manages post search routine
    """
    serializer_class = GetListSerializer
    permission_classes = [PostPermissions]

    def get_queryset(self):
        query = self.request.GET.get("q")

        return Post.objects.filter(
            Q(title__icontains=query)
            |
            Q(excerpt=query)
            |
            Q(text__icontains=query)
        ).order_by(
            "-{}".format(
                BaseModel.Field.created_at
            )
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


class PostCover(APIView):
    """
    Separate view for blog post cover management
    """

    permission_classes = [PostPermissions]

    def get(
            self,
            request: Request,
            slug: str
    ) -> Response:
        """
        Returns post cover
        :param request:
        :param slug:
        :return:
        """

        # Check if target post exists
        try:
            post = Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            return Response(
                status=HTTP_404_NOT_FOUND,
                data={
                    ERROR_KEY:
                        ERROR_MSG_NO_POST
                }
            )
        except Post.MultipleObjectsReturned:
            return Response(
                status=HTTP_422_UNPROCESSABLE_ENTITY,
                data={
                    ERROR_KEY:
                        ERROR_MSG_MULTIPLE_POSTS.format(
                            slug
                        )
                }
            )

        return Response(
            {
                Post.Field.cover: post.cover.url
            },
            status=HTTP_200_OK
        )

    def post(
            self,
            request: Request,
            slug: str
    ) -> Response:
        """
        Post cover creation
        :param request:
        :param slug:
        :return:
        """

        # First check if photo is attached
        try:
            cover = request.data[Post.Field.cover]
        except KeyError:
            return Response(
                status=HTTP_422_UNPROCESSABLE_ENTITY,
                data={
                    ERROR_KEY:
                        ERROR_MSG_NO_IMAGE_ATTACHED
                }
            )

        # Check cover format
        try:
            img = Image.open(cover)
        except PIL.UnidentifiedImageError:
            return Response(
                status=HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                data={
                    ERROR_KEY:
                        ERROR_MSG_UNSUPPORTED_IMAGE_FORMAT
                }
            )
        if img.format not in ["JPEG", "PNG"]:
            return Response(
                status=HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                data={
                    ERROR_KEY:
                        ERROR_MSG_UNSUPPORTED_IMAGE_FORMAT
                }
            )

        # Second check if target post exists
        try:
            post = Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            return Response(
                status=HTTP_404_NOT_FOUND,
                data={
                    ERROR_KEY:
                        ERROR_MSG_NO_POST
                }
            )
        except Post.MultipleObjectsReturned:
            return Response(
                status=HTTP_422_UNPROCESSABLE_ENTITY,
                data={
                    ERROR_KEY:
                        ERROR_MSG_MULTIPLE_POSTS.format(
                            slug
                        )
                }
            )

        post.cover = cover
        post.save()

        return Response(
            status=HTTP_202_ACCEPTED,
        )

    def delete(
            self,
            request: Request,
            slug: str
    ) -> Response:
        """
        Removes post cover
        :param request:
        :param slug:
        :return:
        """

        # Check if target post exists
        try:
            post = Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            return Response(
                status=HTTP_404_NOT_FOUND,
                data={
                    ERROR_KEY:
                        ERROR_MSG_NO_POST
                }
            )
        except Post.MultipleObjectsReturned:
            return Response(
                status=HTTP_422_UNPROCESSABLE_ENTITY,
                data={
                    ERROR_KEY:
                        ERROR_MSG_MULTIPLE_POSTS.format(
                            slug
                        )
                }
            )

        post.cover = None
        post.save()

        return Response(
            status=HTTP_204_NO_CONTENT,
        )
