from rest_framework.permissions import (
    BasePermission, SAFE_METHODS
)


class CommentPermissions(BasePermission):
    """
    Defines access for Comment objects
    """

    def has_permission(self, request, view):
        """
        Define permissions for Tags
        """

        # Everyone has read-only (aka GET) access
        if request.method in SAFE_METHODS:
            return True

        # Staff users and admins can manipulate tags
        return request.user.is_authenticated
