from pydantic import ValidationError
from pyngo import drf_error_details

from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_422_UNPROCESSABLE_ENTITY
)

from ....models import Listing, PriceTag, DayRate

from .constants import (
    ERROR_KEY, ERROR_MSG_UNKNOWN_LISTING
)
from .permissions import PriceTagPermissions
from .serializers import PriceTagSerializer, DayRateSerializer
from .validators import PriceTagValidator


class PriceTagsList(ListCreateAPIView):
    """
    Manages price tags listing and creation
    """

    order_by = PriceTag.Field.start_date
    serializer_class = PriceTagSerializer
    permission_classes = [PriceTagPermissions]

    def get_queryset(self):
        try:
            listing = Listing.objects.get(
                slug=self.kwargs.get(Listing.Field.slug)
            )
            return listing.get_price_tags()
        except Listing.DoesNotExist:
            raise NotFound(
                ERROR_MSG_UNKNOWN_LISTING.format(
                    self.kwargs.get(Listing.Field.slug)
                )
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
            PriceTagValidator.model_validate(request.data)
        except ValidationError as error:
            return Response(
                status=HTTP_422_UNPROCESSABLE_ENTITY,
                # Leave only first error message for every field
                data={
                    ERROR_KEY: drf_error_details(error)
                }
            )

        # Obtain and validate data
        serializer = PriceTagSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        # Get listing slug for price tag
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

        price_tag = PriceTag.objects.create(
            listing=listing,
            **serializer.validated_data
        )

        # And return positive response
        return Response(
            status=HTTP_201_CREATED,
            data=PriceTagSerializer(price_tag).data
        )


class DayRatesList(ListAPIView):
    """
    Manages daily rates listing
    """

    order_by = DayRate.Field.date
    serializer_class = DayRateSerializer

    def get_queryset(self):
        try:
            listing = Listing.objects.get(
                slug=self.kwargs.get(Listing.Field.slug)
            )
            return DayRate.objects.filter(
                listing=listing
            )
        except Listing.DoesNotExist:
            raise NotFound(
                ERROR_MSG_UNKNOWN_LISTING.format(
                    self.kwargs.get(Listing.Field.slug)
                )
            )
