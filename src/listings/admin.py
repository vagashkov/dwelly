from typing import Any

from django.contrib.admin import (
    ModelAdmin, site, StackedInline
)
from django.utils.html import mark_safe

from core.models import Reference

from .models import (
    ObjectType, Category, Amenity, HouseRule,
    Listing, Photo, PriceTag, DayRate,
    Reservation
)

APP_NAME = "listings"


class ReferenceAdmin(ModelAdmin):
    """
    Base admin class for reference objects
    """

    def listings_count(self, reference: Any) -> int:
        return reference.listings.count()

    listings_count.short_description = "Listings"

    list_display = (
        Reference.Field.name,
        Reference.Field.description,
        "listings_count",
    )


class ObjectTypeAdmin(ReferenceAdmin):
    """
    Simple class for editing object types using admin panel
    """
    pass


class HouseRuleAdmin(ReferenceAdmin):
    """
    Simple class for editing house rules using admin panel
    """
    pass


class CategoryAdmin(ModelAdmin):
    """
    Simple class for editing amenity categories using admin panel
    """

    list_display = (
        Reference.Field.name,
        Reference.Field.description,

    )


class AmenityAdmin(ModelAdmin):
    """
    Simple class for editing amenities using admin panel
    """

    def listings_count(self, object_type: Amenity) -> int:
        return object_type.listings.count()

    listings_count.short_description = "Listings"

    list_display = (
        Reference.Field.name,
        Reference.Field.description,
        Amenity.Field.category,
        "listings_count"
    )


class PhotoInline(StackedInline):
    """
    Class to embed photo management
    directly into listing admin page
    """

    model = Photo


class ListingAdmin(ModelAdmin):
    """
    Simple class for editing listings using admin panel
    """

    def photos_count(self, listing):
        return listing.photos.count()

    photos_count.short_description = "Photos"

    def reservations_count(self, listing):
        return listing.reservations.count()

    reservations_count.short_description = "Reservations"

    inlines = (
        PhotoInline,
    )

    prepopulated_fields = {
        Listing.Field.slug: (
            Listing.Field.title,
        )
    }

    list_display = (
        Listing.Field.title,
        Listing.Field.object_type,
        "photos_count",
        "reservations_count",
    )

    list_filter = (
        "{}__name".format(
            Listing.Field.object_type
        ),
    )


class PhotoAdmin(ModelAdmin):
    """
    Simple class for editing listing photos using admin panel
    """

    def get_preview(self, object: Photo) -> str:
        return mark_safe(
            "<img src='{}' />".format(object.get_preview())
        )


class PriceTagAdmin(ModelAdmin):
    """
    Simple class for editing listing price tags using admin panel
    """

    list_display = (
        PriceTag.Field.listing,
        PriceTag.Field.start_date,
        PriceTag.Field.end_date,
        PriceTag.Field.price
    )


class DailyRateAdmin(ModelAdmin):
    """
    Simple class for editing listing price tags using admin panel
    """

    list_display = (
        DayRate.Field.listing,
        DayRate.Field.date,
        DayRate.Field.price
    )


class ReservationAdmin(ModelAdmin):
    """
    Simple class for editing reservations using admin panel
    """

    list_display = (
        Reservation.Field.listing,
        Reservation.Field.user,
        Reservation.Field.check_in,
        Reservation.Field.check_out,
        Reservation.Field.in_progress
    )

    list_filter = (
        "listing__title",
        "user__email",
    )


site.register(ObjectType, ObjectTypeAdmin)
site.register(Category, CategoryAdmin)
site.register(Amenity, AmenityAdmin)
site.register(HouseRule, HouseRuleAdmin)
site.register(Listing, ListingAdmin)
site.register(Photo, PhotoAdmin)
site.register(PriceTag, PriceTagAdmin)
site.register(DayRate, DailyRateAdmin)
site.register(Reservation, ReservationAdmin)
