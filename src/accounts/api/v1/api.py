from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_422_UNPROCESSABLE_ENTITY
)

from ...models import Account
from .serializers import (
    ListSerializer,
    PostSerializer,
    DetailsSerializer
)


class Accounts(ListCreateAPIView):
    """
    Manages user account registration routine
    """

    queryset = Account.objects.all()

    def get_serializer_class(self):
        # defines serializer for selected scenario
        if self.request.method == "GET":
            return ListSerializer
        elif self.request.method == "POST":
            return PostSerializer
        raise MethodNotAllowed(
            self.request.method
        )

    def get_permissions(self):
        # defines permissions for selected scenario
        self.permission_classes = [AllowAny]
        if self.request.method == "GET":
            self.permission_classes = [IsAdminUser]
        return super(Accounts, self).get_permissions()

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


class Details(RetrieveUpdateDestroyAPIView):
    """
    Working with single account object details
    """

    queryset = Account.objects.all()
    lookup_url_kwarg = "id"
    serializer_class = DetailsSerializer
