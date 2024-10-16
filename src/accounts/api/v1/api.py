from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
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

        # data is valid - create new user and return result
        account = serializer.save(request)
        if account:
            json = serializer.data
            # token = Token.objects.create(user=user)
            # json['token'] = token.key
            return Response(
                json,
                status=HTTP_201_CREATED
            )
