from django.conf import settings
from django.http import Http404

from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView
)
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_422_UNPROCESSABLE_ENTITY
)

from ...models import User, Profile
from .permissions import ProfilePermissions
from .serializers import (
    UserPost, ProfilesList,
    ProfileGet, ProfilePatch
)


class Users(CreateAPIView):
    """
    Manages user account registration routine
    """

    serializer_class = UserPost
    permission_classes = [AllowAny]

    def create(
            self,
            request: Request,
            *args: list,
            **kwargs: dict
            ) -> Response:
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


class Profiles(ListAPIView):
    """
    Manages user profile list retrieval
    """

    queryset = Profile.objects.all()
    serializer_class = ProfilesList
    permission_classes = [IsAdminUser]


class ProfileDetails(RetrieveUpdateAPIView):
    """
    Working with single profile object details
    """

    permission_classes = [ProfilePermissions]

    def get_object(self) -> Profile:
        public_id = self.kwargs.get(
            User.Field.public_id
        )
        if public_id:
            user_id = settings.FF3_CIPHER.decrypt(
                public_id
            )
            try:
                profile = User.objects.get(
                    id=user_id
                ).profile
            except User.DoesNotExist:
                raise Http404

            # Check permissions before returning object
            self.check_object_permissions(self.request, profile)
            return profile

        raise Http404

    def get_serializer_class(self) -> ModelSerializer:
        # defines serializer for selected scenario
        if self.request.method == "GET":
            return ProfileGet
        elif self.request.method in ["PATCH", "PUT"]:
            return ProfilePatch
        raise MethodNotAllowed(
            self.request.method
        )
