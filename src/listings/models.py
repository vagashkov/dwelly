from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db.models import (
    CharField, SlugField, TextField,
    BooleanField, PositiveSmallIntegerField,
    DateField, TimeField, ImageField, QuerySet,
    ForeignKey, PROTECT, CASCADE, ManyToManyField
)
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from djmoney.models.fields import MoneyField

from core.models import BaseModel, Reference
from core.utils.dates import daterange_generator
from core.utils.images import convert_image, create_thumbnails

from .constants import (
    ERROR_MSG_NEGATIVE_DAY_RATE,
    ERROR_MSG_OVERLAPPING_DATES
)

User = get_user_model()

APP_NAME = "listings"


class ObjectType(Reference):
    """
    Different listing types (rooms, apartments, huts etc.)
    """

    DEFAULT_NAME = "Apartment"

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
    All the necessaries and pleasantries to live
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


def get_default_object_type() -> int:
    object_type, _ = ObjectType.objects.get_or_create(
        name=ObjectType.DEFAULT_NAME
    )
    return object_type.id


class Listing(BaseModel):
    """
    Rooms, apartments etc.
    """

    class Field:
        # Base info
        object_type: str = "object_type"
        title: str = "title"
        slug: str = "slug"
        description: str = "description"
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
        # Other data
        absolute_url: str = "absolute_url"
        cover_photo: str = "cover_photo"

    LOOKUP_KEY = "slug"

    # Base info
    object_type: ForeignKey = ForeignKey(
        ObjectType,
        null=False,
        blank=False,
        default=get_default_object_type,
        related_name="listings",
        on_delete=PROTECT,
        verbose_name=_("Object type")
    )

    title: CharField = CharField(
        null=False,
        blank=True,
        max_length=64,
        verbose_name=_("Title")
    )

    slug: SlugField = SlugField(
        null=False,
        blank=True,
        unique=True,
        db_index=True,
        verbose_name=_("Slug")
    )

    description: TextField = TextField(
        null=False,
        blank=True,
        default="",
        verbose_name=_("Description")
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

    def __str__(self) -> str:
        return "{} {}".format(
            self.object_type.name,
            self.title
        )

    def get_absolute_url(self) -> str:
        return reverse("listings:listing_details", args=[self.slug])

    def get_cover_photo(self) -> "Photo":
        if self.photos:
            try:
                return self.photos.get(
                    is_cover=True
                )
            except Photo.DoesNotExist:
                pass

    def get_photos(self) -> "QuerySet[Photo]":
        if self.photos:
            return self.photos.order_by(
                Photo.Field.index
            )

    def get_price_tags(self) -> "QuerySet[PriceTag]":
        if self.price_tags:
            return self.price_tags.order_by(
                PriceTag.Field.start_date
            )

    def get_reservations(self) -> "QuerySet[Reservation]":
        if self.reservations:
            return self.reservations.order_by(
                Reservation.Field.check_in
            )


def upload_path(instance: Listing, filename: str) -> str:
    return "{}/{}/{}/{}".format(
        APP_NAME,
        instance.listing.uuid,
        "photos",
        filename
    )


class Photo(BaseModel):
    """
    Class to store listing photos
    """

    class Field:
        index: str = "index"
        title: str = "title"
        file: str = "file"
        listing: str = "listing"
        is_cover: str = "is_cover"

    SORT_KEY = Field.index

    index: PositiveSmallIntegerField = PositiveSmallIntegerField(
        null=False,
        verbose_name=_("Index")
    )

    title: CharField = CharField(
        null=False,
        blank=True,
        default="",
        max_length=64,
        verbose_name=_("Title")
    )

    file: ImageField = ImageField(
        upload_to=upload_path,
        verbose_name=_("File")
    )

    listing: ForeignKey = ForeignKey(
        Listing,
        related_name="photos",
        on_delete=CASCADE,
        verbose_name=_("Listing")
    )

    is_cover: BooleanField = BooleanField(
        null=False,
        blank=True,
        default=False
    )

    def __str__(self) -> str:
        return "{}".format(self.title)

    def save(self, *args: list, **kwargs: dict) -> None:
        # Save original to database and obtain it's storage name
        super().save(*args, **kwargs)

        if self.file:
            # Build image previews if necessary
            if settings.IMAGE_SIZES:
                for size in settings.IMAGE_SIZES:
                    create_thumbnails.delay(
                        self.file.path,
                        size[0],
                        size[1],
                        settings.IMAGE_FORMAT
                    )
            # Convert image format if necessary
            if settings.IMAGE_CONVERT_ORIGINAL:
                convert_image.delay(
                    self.file.path,
                    settings.IMAGE_FORMAT
                )

    def get_preview(self) -> str:
        dot: int = self.file.url.rfind(".")
        file_name: str = self.file.url[:dot]

        return "{}_{}x{}.{}".format(
            file_name,
            str(settings.IMAGE_SIZE_SMALL[0]),
            str(settings.IMAGE_SIZE_SMALL[1]),
            settings.IMAGE_FORMAT
        )

    def get_details(self) -> str:
        dot: int = self.file.url.rfind(".")
        file_name: str = self.file.url[:dot]

        return "{}_{}x{}.{}".format(
            file_name,
            str(settings.IMAGE_SIZE_MEDIUM[0]),
            str(settings.IMAGE_SIZE_MEDIUM[1]),
            settings.IMAGE_FORMAT
        )


class PriceTag(BaseModel):
    """
    Stores listing price for some period
    """

    class Field:
        listing: str = "listing"
        start_date: str = "start_date"
        end_date: str = "end_date"
        price: str = "price"
        description: str = "description"

    listing: ForeignKey = ForeignKey(
        Listing,
        related_name="price_tags",
        on_delete=CASCADE,
        verbose_name=_("Listing")
    )

    start_date: DateField = DateField(
        null=False,
        blank=False,
        verbose_name=_("Start date")
    )

    end_date: DateField = DateField(
        null=False,
        blank=False,
        verbose_name=_("End date")
    )

    price: MoneyField = MoneyField(
        null=False,
        max_digits=19,
        decimal_places=4,
        default_currency=settings.BASE_CURRENCY
    )

    description: CharField = CharField(
        null=False,
        blank=True,
        default="",
        max_length=512,
        verbose_name=_("Description")
    )

    def clean(self):
        overlapping_dates = list()

        # First we have to look for potential conflicts
        for current_date in daterange_generator(
                self.start_date, self.end_date
        ):
            try:
                day_rate = DayRate.objects.get(
                    listing=self.listing,
                    date=current_date,
                )
            except DayRate.DoesNotExist:
                pass
            else:
                if day_rate.price_tag != self:
                    overlapping_dates.append(
                        current_date.strftime("%Y-%m-%d")
                    )

        if overlapping_dates:
            raise ValidationError(
                ERROR_MSG_OVERLAPPING_DATES.format(
                    ", ".join(overlapping_dates)
                )
            )

        if self.price.amount < 0:
            raise ValidationError(
                ERROR_MSG_NEGATIVE_DAY_RATE.format(
                    self.price.amount)
                )

    def __str__(self) -> str:
        return "{} - {}: {}".format(
            self.start_date.strftime("%b %d, %Y"),
            self.end_date.strftime("%b %d, %Y"),
            self.price
        )


class DayRate(BaseModel):
    """
    Stores listing price for some precise date
    """

    class Field:
        listing: str = "listing"
        price_tag: str = "price_tag"
        date: str = "date"
        price: str = "price"
        description: str = "description"

    listing: ForeignKey = ForeignKey(
        Listing,
        related_name="day_rates",
        on_delete=CASCADE,
        verbose_name=_("Listing")
    )

    price_tag: ForeignKey = ForeignKey(
        PriceTag,
        related_name="day_rates",
        on_delete=CASCADE,
        verbose_name=_("Price tag")
    )

    date: DateField = DateField(
        null=False,
        blank=False,
        verbose_name=_("Date")
    )

    price: MoneyField = MoneyField(
        null=False,
        max_digits=19,
        decimal_places=4,
        default_currency=settings.BASE_CURRENCY
    )

    description: CharField = CharField(
        null=False,
        blank=True,
        default="",
        max_length=512,
        verbose_name=_("Description")
    )

    def __str__(self) -> str:
        return "{} on {}: {}".format(
            self.listing.title,
            self.date.strftime("%b %d, %Y"),
            self.price
        )


class Reservation(BaseModel):
    """
    Class for listing reservations made by users
    """

    class Field:
        user: str = "user"
        listing: str = "listing"
        check_in: str = "check_in"
        check_out: str = "check_out"
        in_progress: str = "in_progress"
        comment: str = "comment"

    user: ForeignKey = ForeignKey(
        User,
        null=False,
        related_name="reservations",
        verbose_name=_("User"),
        on_delete=CASCADE
    )

    listing: ForeignKey = ForeignKey(
        Listing,
        null=False,
        verbose_name=_("Listing"),
        related_name="reservations",
        on_delete=CASCADE
    )

    check_in: DateField = DateField(
        null=False,
        blank=False,
        verbose_name=_("Check-in")
    )

    check_out: DateField = DateField(
        null=False,
        blank=False,
        verbose_name=_("Check-out")
    )

    comment: TextField = TextField(
        null=False,
        blank=True,
        default="",
        verbose_name=_("Comment")
    )

    def __str__(self):
        return "{} {}-{}".format(
            self.listing.title,
            self.check_in,
            self.check_out
        )

    def in_progress(self):
        return self.check_in < now().date() < self.check_out

    in_progress.boolean = True
