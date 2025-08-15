from pydantic import ValidationError
from pyngo import drf_error_details

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_422_UNPROCESSABLE_ENTITY
)

from core.api.paginators import BasePaginator

from ...constants import ERROR_KEY, LISTINGS_ORDERING
from ...models import Listing

from .permissions import ListingPermissions
from .serializers import (
    GetListingDigest, GetListingDetails, PostListingSerializer
)
from .validators import PostListing


class Listings(ListCreateAPIView):
    """
    Manages object types listing and new object types creation
    """

    serializer_class = GetListingDigest
    pagination_class = BasePaginator
    permission_classes = [ListingPermissions]

    def get_queryset(self):
        return Listing.objects.all().order_by(
            LISTINGS_ORDERING
        )

    def create(
            self,
            request: Request,
            *args: list,
            **kwargs: dict
    ) -> Response:
        """
        New listing creation routine
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        # First, validate data using pydantic class
        try:
            PostListing.model_validate(request.data)
        except ValidationError as error:
            return Response(
                status=HTTP_422_UNPROCESSABLE_ENTITY,
                # Leave only first error message for every field
                data={
                    ERROR_KEY: drf_error_details(error)
                }
            )

        # Obtain and validate data
        serializer = PostListingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create new Listing instance
        self.perform_create(serializer)

        # Send response including the created instance details
        headers = self.get_success_headers(serializer.data)
        return Response(
            GetListingDetails(serializer.instance).data,
            status=HTTP_201_CREATED,
            headers=headers
        )


class ListingDetails(RetrieveUpdateDestroyAPIView):
    """
    Manages single object type instance lifecycle
    """

    queryset = Listing.objects.all()
    lookup_field = Listing.Field.slug
    lookup_url_kwarg = Listing.Field.slug
    serializer_class = GetListingDetails
    permission_classes = [ListingPermissions]
