from pydantic import ValidationError
from rest_framework.generics import ListCreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY
)

from .....constants import (
    COMMENTS_ORDERING,
    ERROR_KEY,
    ERROR_MSG_NO_POST_SLUG,
    ERROR_MSG_NO_POST,
    ERROR_MSG_MULTIPLE_POSTS
)
from .....models import Post, Comment

from .paginators import CommentsPaginator
from .permissions import CommentPermissions
from .serializers import GetComments, PostComment
from .validators import CommentValidator


class Comments(ListCreateAPIView):
    """
    Manages post comments listing and new comment creation
    """

    queryset = Comment.objects.all()
    order_by = COMMENTS_ORDERING
    pagination_class = CommentsPaginator
    permission_classes = [CommentPermissions]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PostComment
        return GetComments

    def create(
            self,
            request: Request,
            *args: list,
            **kwargs: dict
    ) -> Response:
        """
        Manages new post comment creation routine
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        # First, validate data using pydantic class
        try:
            CommentValidator.parse_obj(request.data)
        except ValidationError as error:
            return Response(
                status=HTTP_422_UNPROCESSABLE_ENTITY,
                data={
                    ERROR_KEY: error.errors()
                }
            )

        # Deserialize and check data
        serializer = PostComment(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Obtain parent post slug
        slug = kwargs.get(Post.Field.slug)

        # Check if parent post slug included in request parameters
        if slug is None:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={
                    ERROR_KEY: ERROR_MSG_NO_POST_SLUG
                }
            )

        # Check if target post exists
        try:
            post = Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            return Response(
                status=HTTP_404_NOT_FOUND,
                data={
                    ERROR_KEY: ERROR_MSG_NO_POST
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

        serializer.save(
            post=post,
            author=self.request.user
        )

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=HTTP_201_CREATED,
            headers=headers
        )

    def list(
            self,
            request: Request,
            *args: list,
            **kwargs: dict
    ) -> Response:
        """
        Returns post comments list
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        # Obtain parent post slug
        slug = kwargs.get(Post.Field.slug)

        # Check if parent post slug included in request parameters
        if slug is None:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={
                    ERROR_KEY: ERROR_MSG_NO_POST_SLUG
                }
            )

        # Check if target post exists
        try:
            post = Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            return Response(
                status=HTTP_404_NOT_FOUND,
                data={
                    ERROR_KEY: ERROR_MSG_NO_POST
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

        queryset = post.comments.all().order_by(
            COMMENTS_ORDERING
        )

        # Should we use pagination?
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = GetComments(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = GetComments(queryset, many=True)
        return Response(serializer.data)
