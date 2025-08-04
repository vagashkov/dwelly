from rest_framework.request import Request
from rest_framework.permissions import (
    BasePermission, SAFE_METHODS
)
from rest_framework.views import APIView


class CommentPermissions(BasePermission):
    """
    Defines access for Comment objects
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        """
        Define permissions for Tags
        """

        # Everyone has read-only (aka GET) access
        if request.method in SAFE_METHODS:
            return True

        # Staff users and admins can manipulate tags
        return request.user.is_authenticated
