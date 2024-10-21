from django.contrib.admin import site, StackedInline
from django.contrib.auth.admin import UserAdmin

from .forms import Signup
from .models import Account, Profile


class ProfileInline(StackedInline):
    model = Profile
    can_delete = True
    verbose_name = Profile


class AccountsAdmin(UserAdmin):
    """
    Defines user display and manipulation in admin panel
    """

    model = Account

    add_form = Signup

    inlines = (ProfileInline,)

    # Fields displayed in users list
    list_display = [
        Account.Field.email,
        Account.Field.last_login,
    ]

    ordering = (
        Account.Field.email,
    )

    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    Account.Field.email,
                    "{}1".format(Account.Field.password),
                    "{}2".format(Account.Field.password),
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
                    Account.Field.email,
                    Account.Field.date_joined,
                    Account.Field.password,
                    Account.Field.last_login
                )
            }
        ),

        # Groups and permission section
        (
            "Details",
            {
                "fields": (
                    Account.Field.is_active,
                    Account.Field.is_staff,
                    Account.Field.is_superuser,
                    "groups",
                    "user_permissions"
                )
            }
        ),
    )


site.register(Account, AccountsAdmin)
