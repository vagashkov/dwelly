from django.contrib.auth import get_user_model
from django.db.models import (
    CharField, TextField, TimeField,
    BooleanField, PositiveSmallIntegerField,
    ForeignKey, PROTECT, ManyToManyField
)
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField

from config.settings import DEFAULT_COUNTRY
from core.models import BaseModel, Reference

User = get_user_model()


def get_default_object_type():
    object_type, _ = ObjectType.objects.get_or_create(
        name=ObjectType.DEFAULT_NAME
    )
    return object_type.id


def get_default_host():
    return User.objects.filter(is_superuser=True)[0]


class ObjectType(Reference):
    """
    Different listing types
    """

    class Meta:
        verbose_name = "Object type"


class Category(Reference):
    """
    Amenities category
    """

    class Meta:
        verbose_name_plural = "Categories"


class Amenity(Reference):
    """

    """

    class Field:
        name: str = "name"
        description: str = "description"
        category: str = "category"

    category: ForeignKey = ForeignKey(
        Category,
        blank=False,
        related_name="amenities",
        on_delete=PROTECT,
        verbose_name=_("Category")
    )

    class Meta:
        verbose_name_plural = "Amenities"


class HouseRule(Reference):
    """
    Class for different house rules (no smoking etc.)
    """

    class Meta:
        verbose_name = "House rule"


class Listing(BaseModel):
    """
    Listing model class
    """

    class Field:
        # Base info
        object_type: str = "object_type"
        title: str = "title"
        description: str = "description"
        # Location info
        country: str = "country"
        city: str = "city"
        address: str = "address"
        # Capacity
        max_guests: str = "max_guests"
        bedrooms: str = "bedrooms"
        beds: str = "beds"
        bathrooms: str = "bathrooms"
        # Add-ons
        amenities: str = "amenities"
        house_rules: str = "house_rules"
        # Reservation
        check_in_time: str = "check_in_time"
        check_out_time: str = "check_out_time"
        instant_booking: str = "instant_booking"
        hosts: str = "hosts"

    # Base info
    object_type: ForeignKey = ForeignKey(
        ObjectType,
        null=False,
        blank=False,
        related_name="listings",
        on_delete=PROTECT,
        verbose_name=_("Object type")
    )

    title: CharField = CharField(
        null=False,
        blank=False,
        max_length=64,
        verbose_name=_("Title")
    )

    description: TextField = TextField(
        null=False,
        blank=True,
        default="",
        verbose_name=_("Description")
    )

    # Location info
    country: CountryField = CountryField(
        null=False,
        blank=True,
        blank_label="(select country)",
        default=DEFAULT_COUNTRY,
        verbose_name=_("Country")
    )

    city: CharField = CharField(
        null=False,
        blank=True,
        max_length=64,
        verbose_name=_("City")
    )

    address: CharField = CharField(
        null=False,
        blank=True,
        default="",
        verbose_name=_("Address")
    )

    # Capacity
    max_guests: PositiveSmallIntegerField = PositiveSmallIntegerField(
        null=False,
        blank=False,
        default=1,
        verbose_name=_("Max guests")
    )

    bedrooms: PositiveSmallIntegerField = PositiveSmallIntegerField(
        null=False,
        blank=False,
        default=1,
        verbose_name=_("Bedrooms")
    )

    beds: PositiveSmallIntegerField = PositiveSmallIntegerField(
        null=False,
        blank=False,
        default=1,
        verbose_name=_("Beds")
    )

    bathrooms: PositiveSmallIntegerField = PositiveSmallIntegerField(
        null=False,
        blank=False,
        default=1,
        verbose_name=_("Bathrooms")
    )

    # Add-ons
    amenities: ManyToManyField = ManyToManyField(
        Amenity,
        blank=True,
        related_name="listings",
        verbose_name=_("Amenities")
    )

    house_rules: ManyToManyField = ManyToManyField(
        HouseRule,
        blank=True,
        related_name="listings",
        verbose_name=_("House rules")
    )

    # Reservation
    check_in_time: TimeField = TimeField(
        null=True,
        verbose_name=_("Check-in time")
    )

    check_out_time: TimeField = TimeField(
        null=True,
        verbose_name=_("Check-out time")
    )

    instant_booking: BooleanField = BooleanField(
        null=False,
        default=False,
        verbose_name=_("Instant booking")
    )

    hosts: ManyToManyField = ManyToManyField(
        User,
        related_name="listings",
        verbose_name=_("Hosts")
    )

    def __str__(self):
        return "{} ({}, {})".format(
            self.title,
            self.city,
            self.country
        )
