from rest_framework.request import Request
from rest_framework.permissions import (
    BasePermission, SAFE_METHODS
)
from rest_framework.views import APIView

from ...models import Profile


class ProfilePermissions(BasePermission):
    """
    Defines access for profile object update
    """

    def has_object_permission(
            self,
            request: Request,
            view: APIView,
            obj: Profile
    ) -> bool:
        """
        Users can edit only their own profiles
        """

        # admins are omnipotent
        if request.user.is_superuser:
            return True

        # staff members can access user profiles
        if request.user.is_staff and (request.method in SAFE_METHODS):
            return True

        # standard users can access their own profiles
        return request.user.id == obj.user.id
