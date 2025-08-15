from typing import Any

from django.contrib.admin import (
    ModelAdmin, site, StackedInline
)
from django.utils.html import mark_safe

from core.models import Reference

from .models import (
    ObjectType, Category, Amenity,
    HouseRule, Listing, Photo, PriceTag
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


site.register(ObjectType, ObjectTypeAdmin)
site.register(Category, CategoryAdmin)
site.register(Amenity, AmenityAdmin)
site.register(HouseRule, HouseRuleAdmin)
site.register(Listing, ListingAdmin)
site.register(Photo, PhotoAdmin)
site.register(PriceTag, PriceTagAdmin)
