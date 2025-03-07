from django.contrib.admin import site
from django.contrib.auth.admin import UserAdmin

from .models import Account


class AccountsAdmin(UserAdmin):
    """
    Defines user accounts display and manipulation
    options via admin panel
    """

    model = Account

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
