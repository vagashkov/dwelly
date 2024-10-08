from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)
from django.db.models import (
    BooleanField, EmailField, DateTimeField
)
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from core.models import BaseModel

from .managers import AccountManager

APP_NAME = "accounts"


class Account(AbstractBaseUser, PermissionsMixin, BaseModel):
    """
    Custom user account model
    """

    # define user model attributes list
    class Field:
        # IDs
        id: str = "id"
        uuid: str = "uuid"

        # Authorization data
        email: str = "email"
        password: str = "password"

        # Account status
        is_active: str = "is_active"
        is_staff: str = "is_staff"
        is_superuser: str = "is_superuser"
        date_joined: str = "date_joined"
        last_login: str = "last_login"

        # Account record data
        created_at: str = "created_at"
        updated_at: str = "updated_at"

    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")

    objects = AccountManager()

    # users are identified by email
    USERNAME_FIELD = Field.email
    # and it is the only (except password) field
    # needed to create an account
    REQUIRED_FIELDS = []

    email = EmailField(
        null=False,
        blank=False,
        unique=True,
        max_length=320,
        verbose_name=_("Email")
    )

    is_active = BooleanField(
        default=True,
        verbose_name=_("Is active")
    )

    is_staff = BooleanField(
        default=False,
        verbose_name=_("Is staff")
    )

    is_superuser = BooleanField(
        default=False,
        verbose_name=_("Is superuser")
    )

    date_joined = DateTimeField(
        default=timezone.now
    )

    def __str__(self):
        """ Object string representation """
        return self.email
