from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)
from django.db.models import (
    BooleanField, ImageField,
    CharField, EmailField, TextField,
    DateField, DateTimeField,
    OneToOneField, CASCADE
)
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField

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
        password1: str = "password1"
        password2: str = "password2"

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

    objects: AccountManager = AccountManager()

    # users are identified by email
    EMAIL_FIELD: str = Field.email
    USERNAME_FIELD: str = Field.email
    # and it is the only (except password) field
    # needed to create an account
    REQUIRED_FIELDS: list = []

    email: EmailField = EmailField(
        null=False,
        blank=False,
        unique=True,
        max_length=320,
        verbose_name=_("Email")
    )

    is_active: BaseModel = BooleanField(
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
def upload_path(instance, filename):
    return "{}/{}/{}/{}".format(
        APP_NAME,
        instance.uuid,
        "photos",
        filename
    )


class Profile(BaseModel):
    """
    Manages storing additional user info aka "profile"
    """

    # define profile attributes list
    class Field:
        account: str = "account"

        first_name: str = "first_name"
        last_name: str = "last_name"
        full_name: str = "full_name"
        phone: str = "phone"
        country: str = "country"
        language: str = "language"
        birth_date: str = "birth_date"
        bio: str = "bio"
        photo: str = "photo"

    account: OneToOneField = OneToOneField(
        Account,
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

    country: CountryField = CountryField(
        null=False,
        blank=True,
        blank_label="(select country)",
        default="",
        verbose_name=_("Country")
    )

    language: CharField = CharField(
        null=False,
        blank=True,
        max_length=len(settings.DEFAULT_LANGUAGE),
        choices=settings.LANGUAGE_CHOICES,
        verbose_name=_("Language")
    )

    birth_date: DateField = DateField(
        null=True,
        blank=True,
        auto_now=False,
        auto_now_add=False,
        verbose_name=_("Birthdate")
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

    def full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "{} {}".format(
            self.first_name,
            self.last_name
        )
        return full_name.strip()
