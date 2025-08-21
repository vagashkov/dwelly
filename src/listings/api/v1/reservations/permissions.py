from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class ReservationPermissions(BasePermission):
    """
    Defines access for Reservation objects
    """

    def has_permission(
            self,
            request: Request,
            view: APIView
    ) -> bool:
        """
        Define permissions for Amenity
        """

        return request.user.is_authenticated
