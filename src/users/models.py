from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)
from django.db.models import (
    CharField, EmailField, TextField,
    BooleanField, DateTimeField,
    OneToOneField, CASCADE, ImageField
)
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from core.models import BaseModel
from core.utils.images import create_thumbnails

from .constants import AVATAR_DIMENSIONS
from .managers import UserManager

APP_NAME = "users"


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    """
    Custom user account model that uses only email and password
    for registration/authentication
    """

    # Define user model attributes list
    class Field:
        # Base entity data
        id: str = "id"
        public_id: str = "public_id"
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


# define location for storing users photo
def upload_path(instance: "Profile", filename: str) -> str:
    return "{}/{}/{}/{}".format(
        APP_NAME,
        instance.user.uuid,
        "photos",
        filename
    )


class Profile(BaseModel):
    """
    Manages storing additional user info aka "profile"
    """

    # define profile attributes list
    class Field:
        user: str = "user"
        first_name: str = "first_name"
        last_name: str = "last_name"
        full_name: str = "full_name"
        phone: str = "phone"
        bio: str = "bio"
        photo: str = "photo"
        reservations_count: str = "reservations_count"

    user: OneToOneField = OneToOneField(
        User,
        related_name="profile",
        on_delete=CASCADE
    )

    first_name = CharField(
        null=False,
        blank=True,
        default="",
        max_length=150,
        verbose_name=_("First name")
    )

    last_name = CharField(
        null=False,
        blank=True,
        default="",
        max_length=150,
        verbose_name=_("Last name")
    )

    phone: PhoneNumberField = PhoneNumberField(
        null=False,
        blank=True,
        default="",
        verbose_name=_("Phone")
    )

    bio: TextField = TextField(
        null=False,
        blank=True,
        default="",
        verbose_name=_("Bio")
    )

    photo: ImageField = ImageField(
        null=True,
        blank=True,
        verbose_name=_("Photo"),
        upload_to=upload_path
    )

    def full_name(self) -> str:
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "{} {}".format(
            self.first_name,
            self.last_name
        )
        return full_name.strip()

    def get_absolute_url(self) -> str:
        return reverse(
            "profile",
            kwargs={
                "public_id": self.public_id
            }
        )

    def __str__(self) -> str:
        """ Object string representation """
        return "{}".format(self.full_name())

    def save(self,
             *args: list,
             **kwargs: dict
             ) -> None:
        # Save original to database and obtain it's storage name
        super().save(*args, **kwargs)

        if self.photo:
            # Perform necessary routines (resize)
            for size in AVATAR_DIMENSIONS:
                create_thumbnails(
                    settings.MEDIA_ROOT.joinpath(
                        self.photo.name
                    ),
                    *AVATAR_DIMENSIONS.get(size),
                    settings.IMAGE_FORMAT
                )

    def reservations_count(self):
        return self.user.reservations.count()

    reservations_count.short_description = "Reservations"
