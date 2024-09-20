from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Account


class AccountsAdmin(UserAdmin):
    """
    Defines user display and manipulation in admin panel
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


admin.site.register(Account, AccountsAdmin)
