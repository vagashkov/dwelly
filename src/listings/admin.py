from django.contrib.admin import (
    ModelAdmin, site
)

from core.models import Reference

from .models import (
    ObjectType, Category, Amenity, HouseRule
)

APP_NAME = "listings"


class ObjectTypeAdmin(ModelAdmin):
    """
    Simple class for editing object types using admin panel
    """

    list_display = (
        Reference.Field.name,
        Reference.Field.description
    )


class CategoryAdmin(ModelAdmin):
    """
    Simple class for editing amenity categories using admin panel
    """

    list_display = (
        Reference.Field.name,
        Reference.Field.description
    )


class AmenityAdmin(ModelAdmin):
    """
    Simple class for editing amenities using admin panel
    """

    list_display = (
        Reference.Field.name,
        Reference.Field.description
    )


class HouseRuleAdmin(ModelAdmin):
    """
    Simple class for editing house rules using admin panel
    """

    list_display = (
        Reference.Field.name,
        Reference.Field.description
    )


site.register(ObjectType, ObjectTypeAdmin)
site.register(Category, CategoryAdmin)
site.register(Amenity, AmenityAdmin)
site.register(HouseRule, HouseRuleAdmin)
