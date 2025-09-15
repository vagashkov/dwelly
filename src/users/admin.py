from django.contrib.admin import site, StackedInline
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Profile

User = get_user_model()


class ProfileInline(StackedInline):
    model = Profile
    can_delete = True
    verbose_name = Profile


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

    inlines = (
        ProfileInline,
    )

    ordering = (
        User.Field.email,
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    User.Field.email,
                    "{}1".format(User.Field.password),
                    "{}2".format(User.Field.password),
                    User.Field.is_active,
                    User.Field.is_staff,
                    User.Field.is_superuser
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
                    User.Field.password,
                )
            }
        ),

        # Groups and permission section
        (
            _("Details"),
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

        (
            _("History"),
            {
                "fields": (
                    User.Field.date_joined,
                    User.Field.last_login
                )
            }
        ),
    )

    readonly_fields = [
        User.Field.date_joined,
        User.Field.last_login
    ]


site.register(User, UsersAdmin)
