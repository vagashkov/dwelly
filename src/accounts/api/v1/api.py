from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_422_UNPROCESSABLE_ENTITY
)

from .serializers import PostSerializer


class RegisterAccount(CreateAPIView):
    """
    Manages user account registration routine
    """

    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        # extract and validate request data
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            return Response(
                status=HTTP_422_UNPROCESSABLE_ENTITY,
                data={
                    key: value for (key, value) in serializer.errors.items()
                }
            )
