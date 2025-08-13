from rest_framework.generics import ListCreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_422_UNPROCESSABLE_ENTITY
)

from .constants import (
    ERROR_KEY,
    ERROR_MSG_NO_PHOTO_ATTACHED,
    ERROR_MSG_NO_PHOTO_INDEX,
    ERROR_MSG_NO_PHOTO_TITLE,
    ERROR_MSG_UNKNOWN_LISTING
)
from ....models import Listing, Photo

from .permissions import PhotoPermissions
from .serializers import PhotoSerializer


class PhotosList(ListCreateAPIView):
    """
    Manages listing photo creation
    """

    order_by = Photo.Field.index
    permission_classes = [PhotoPermissions]

    def post(
            self,
            request: Request,
            *args: list,
            **kwargs: dict
    ) -> Response:
        """
        :param public_id:
        :param request:
        :return:
        """

        # First check if photo is attached
        try:
            file = request.data[Photo.Field.file]
        except KeyError:
            return Response(
                status=HTTP_422_UNPROCESSABLE_ENTITY,
                data={
                    ERROR_KEY: ERROR_MSG_NO_PHOTO_ATTACHED
                }
            )

        # Check if photo index included
        try:
            index = int(request.data[Photo.Field.index])
        except KeyError:
            return Response(
                status=HTTP_422_UNPROCESSABLE_ENTITY,
                data={
                    ERROR_KEY: ERROR_MSG_NO_PHOTO_INDEX
                }
            )
        except ValueError:
            return Response(
                status=HTTP_422_UNPROCESSABLE_ENTITY,
                data={
                    ERROR_KEY: ERROR_MSG_NO_PHOTO_INDEX
                }
            )

        title = request.data.get(Photo.Field.title)
        if not title:
            return Response(
                status=HTTP_422_UNPROCESSABLE_ENTITY,
                data={
                    ERROR_KEY: ERROR_MSG_NO_PHOTO_TITLE
                }
            )

        is_cover = request.data.get(Photo.Field.is_cover, False)

        # Then check if listing id for photo provided
        slug = self.kwargs.get(
            Listing.Field.slug
        )

        # And check if listing exists in database
        try:
            listing = Listing.objects.get(
                slug=slug
            )
        except Listing.DoesNotExist:
            return Response(
                status=HTTP_422_UNPROCESSABLE_ENTITY,
                data={
                    ERROR_KEY: ERROR_MSG_UNKNOWN_LISTING
                }
            )

        photo_object = Photo.objects.create(
            listing=listing,
            file=file,
            index=index,
            title=title,
            is_cover=is_cover
        )

        # And return positive response
        return Response(
            status=HTTP_201_CREATED,
            data=PhotoSerializer(photo_object).data
        )
