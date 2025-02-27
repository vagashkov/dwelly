from django.contrib.admin import (
    ModelAdmin, site
)

from core.models import Reference

from .models import (
    ObjectType, Category, Amenity, HouseRule, Listing
)

APP_NAME = "listings"


class ReferenceAdmin(ModelAdmin):
    """
    Base admin class for reference objects
    """
    def listings_count(self, object_type):
        return object_type.listings.count()

    listings_count.short_description = "Listings"

    list_display = (
        Reference.Field.name,
        Reference.Field.description,
        "listings_count"
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

    def listings_count(self, object_type):
        return object_type.listings.count()

    listings_count.short_description = "Listings"

    list_display = (
        Reference.Field.name,
        Reference.Field.description,
        "category",
        "listings_count",
    )


class ListingAdmin(ModelAdmin):
    """
    Simple class for editing listings using admin panel
    """

    list_display = (
        Listing.Field.title,
        Listing.Field.object_type,
        Listing.Field.country,
        Listing.Field.city
    )

    list_filter = (
        "{}__name".format(
            Listing.Field.object_type
        ),
        Listing.Field.country,
    )


site.register(ObjectType, ObjectTypeAdmin)
site.register(Category, CategoryAdmin)
site.register(Amenity, AmenityAdmin)
site.register(HouseRule, HouseRuleAdmin)
site.register(Listing, ListingAdmin)
