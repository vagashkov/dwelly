from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)
from django.db.models import (
    EmailField, BooleanField, DateTimeField
)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    """
    Custom user account model that uses only email and password
    for registration/authentication
    """

    # Define user model attributes list
    class Field:
        # Base entity data
        id: str = "id"
        created_at: str = "created_at"
        updated_at: str = "updated_at"

        # Authorization data
        email: str = "email"
        password: str = "password"

        # Account status data
        is_active: str = "is_active"
        is_staff: str = "is_staff"
        is_superuser: str = "is_superuser"
        date_joined: str = "date_joined"
        last_login: str = "last_login"

    class Meta:
        verbose_name = _("User")

    # users are identified by email
    EMAIL_FIELD: str = Field.email
    USERNAME_FIELD: str = Field.email
    # and it is the only (except password) field
    # needed to create user account
    REQUIRED_FIELDS: list = []

    objects: UserManager = UserManager()

    email: EmailField = EmailField(
        null=False,
        blank=False,
        unique=True,
        max_length=320,
        verbose_name=_("Email")
    )

    is_active: BooleanField = BooleanField(
        default=True,
        verbose_name=_("Is active")
    )

    is_staff: BooleanField = BooleanField(
        default=False,
        verbose_name=_("Is staff")
    )

    is_superuser: BooleanField = BooleanField(
        default=False,
        verbose_name=_("Is superuser")
    )

    date_joined: DateTimeField = DateTimeField(
        default=timezone.now
    )

    def __str__(self) -> str:
        """ Object string representation """
        return "{}".format(self.email)
