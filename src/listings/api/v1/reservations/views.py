from pydantic import ValidationError
from pyngo import drf_error_details

from rest_framework.exceptions import NotFound
from rest_framework.generics import ListCreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_422_UNPROCESSABLE_ENTITY
)

from ....models import Listing, Reservation

from ..constants import (
    ERROR_KEY, ERROR_MSG_UNKNOWN_LISTING
)

from .permissions import ReservationPermissions
from .serializers import ReservationSerializer
from .validators import ReservationValidator


class ListingReservations(ListCreateAPIView):
    """
    Manages reservations listing and creation
    """

    order_by = Reservation.Field.check_in
    serializer_class = ReservationSerializer
    permission_classes = [ReservationPermissions]

    def get_queryset(self):
        try:
            listing = Listing.objects.get(
                slug=self.kwargs.get(Listing.Field.slug)
            )
            return listing.get_reservations()
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
            ReservationValidator.model_validate(request.data)
        except ValidationError as error:
            return Response(
                status=HTTP_422_UNPROCESSABLE_ENTITY,
                # Leave only first error message for every field
                data={
                    ERROR_KEY: drf_error_details(error)
                }
            )

        # Obtain and validate data
        serializer = ReservationSerializer(
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

        reservation = Reservation.objects.create(
            listing=listing,
            user=request.user,
            **serializer.validated_data
        )

        # And return positive response
        return Response(
            status=HTTP_201_CREATED,
            data=ReservationSerializer(
                reservation
            ).data
        )
