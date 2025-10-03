from django.db.models import (
    CharField, TextField, BooleanField,
    ForeignKey, CASCADE, PROTECT
)
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField

from core.models import BaseModel, BaseContact, Reference


class Company(BaseModel):
    """
    Manages company info storing and display
    """

    class Meta:
        verbose_name_plural = "Companies"

    class Field:
        full_name: str = "full_name"
        short_name: str = "short_name"
        license: str = "license"
        registration: str = "registration"

    full_name: CharField = CharField(
        null=False,
        blank=True,
        default="",
        max_length=256,
        verbose_name=_("Full name")
    )

    short_name: CharField = CharField(
        null=False,
        blank=True,
        default="",
        max_length=64,
        verbose_name=_("Short name")
    )

    license: CharField = CharField(
        null=False,
        blank=True,
        default="",
        max_length=256,
        verbose_name=_("License")
    )

    registration: CharField = CharField(
        null=False,
        blank=True,
        default="",
        max_length=256,
        verbose_name=_("Registration")
    )

    def __str__(self) -> str:
        return "{} ({})".format(
            self.full_name,
            self.short_name
        )


class CompanyAddress(BaseModel):
    """
    Manages storing physical addresses (postal, office etc).
    for different kinds of entities
    """

    class Meta:
        verbose_name_plural = "Addresses"

    class Field:
        company: str = "company"
        country: str = "country"
        city: str = "city"
        street_address: str = "street_address"
        zip_code: str = "zip_code"
        description: str = "description"

    company: ForeignKey = ForeignKey(
        Company,
        null=False,
        blank=False,
        on_delete=CASCADE,
        related_name="addresses",
        verbose_name=_("Company")
    )

    country: CountryField = CountryField()

    city: CharField = CharField(
        null=False,
        blank=True,
        default="",
        max_length=64,
        verbose_name=_("City")
    )

    street_address: CharField = CharField(
        null=False,
        blank=True,
        default="",
        max_length=256,
        verbose_name=_("Street address")
    )

    zip_code: CharField = CharField(
        null=False,
        blank=True,
        default="",
        max_length=12,
        verbose_name=_("Zip code")
    )

    def __str__(self) -> str:
        return "{} {}, {}, {}".format(
            self.zip_code,
            self.street_address,
            self.city,
            self.country
        )


class ContactType(Reference):
    """
    Manages storing different contact info types
    (email, phone, WhatsApp, Telegram etc.)
    """

    class Meta:
        verbose_name_plural = "Contact types"


class CompanyContact(BaseContact):
    """
    Manages storing company contacts (email, Telegram, WhatsApp etc).
    """

    class Field:
        company: str = "company"
        contact_type: str = "contact_type"
        value: str = "value"
        description: str = "description"

    class Meta:
        verbose_name_plural = "Contacts"

    contact_type: ForeignKey = ForeignKey(
        ContactType,
        null=False,
        blank=False,
        on_delete=PROTECT,
        verbose_name=_("Contact type")
    )

    company: ForeignKey = ForeignKey(
        Company,
        null=False,
        blank=False,
        on_delete=CASCADE,
        related_name="contacts",
        verbose_name=_("Company")
    )


class UserMessage(BaseModel):
    """
    Class for contact form messages
    """

    class Meta:
        verbose_name_plural = _("User messages")

    class Field:
        author: str = "author"
        contact_type: str = "contact_type"
        contact: str = "contact"
        text: str = "text"
        is_processed: str = "is_processed"

    author: CharField = CharField(
        null=False,
        blank=False,
        max_length=64,
        verbose_name=_("Author")
    )

    contact_type: ForeignKey = ForeignKey(
        ContactType,
        null=False,
        blank=False,
        on_delete=PROTECT,
        verbose_name=_("Contact type")
    )

    contact: CharField = CharField(
        null=False,
        blank=False,
        max_length=256,
        verbose_name=_("Contact")
    )

    text: TextField = TextField(
        null=False,
        blank=False,
        verbose_name=_("Text")
    )

    is_processed: BooleanField = BooleanField(
        null=False,
        blank=True,
        default=False,
        verbose_name=_("Processed")
    )

    def __str__(self) -> str:
        return "{} on {}".format(
            self.author,
            self.created_at
        )
