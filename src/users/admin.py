from django.contrib.admin import site
from django.contrib.auth.admin import UserAdmin

from .models import User


class UsersAdmin(UserAdmin):
    """
    Defines user accounts display and manipulation
    options via admin panel
    """

    model = User

    # Fields displayed in users list
    list_display = [
        User.Field.email,
        User.Field.last_login,
    ]

    ordering = (
        User.Field.email,
    )

    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    User.Field.email,
                    "{}1".format(User.Field.password),
                    "{}2".format(User.Field.password),
                ),
                }
        ),
    )

    # Fields displayed on user page
    fieldsets = (
        # Personal data section
        (
            None,
            {
                "fields": (
                    User.Field.email,
                    User.Field.date_joined,
                    User.Field.password,
                    User.Field.last_login
                )
            }
        ),

        # Groups and permission section
        (
            "Details",
            {
                "fields": (
                    User.Field.is_active,
                    User.Field.is_staff,
                    User.Field.is_superuser,
                    "groups",
                    "user_permissions"
                )
            }
        ),
    )


site.register(User, UsersAdmin)
