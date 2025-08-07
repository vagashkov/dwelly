from django.contrib.admin import (
    ModelAdmin, site
)

from core.models import Reference

from .models import (
    ObjectType, Category, Amenity,
    HouseRule,
)

APP_NAME = "listings"


class ReferenceAdmin(ModelAdmin):
    """
    Base admin class for reference objects
    """

    list_display = (
        Reference.Field.name,
        Reference.Field.description,
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

    list_display = (
        Reference.Field.name,
        Reference.Field.description,
        Amenity.Field.category,
    )


site.register(ObjectType, ObjectTypeAdmin)
site.register(Category, CategoryAdmin)
site.register(Amenity, AmenityAdmin)
site.register(HouseRule, HouseRuleAdmin)
