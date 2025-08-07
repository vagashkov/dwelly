from django.db.models import (
    ForeignKey, PROTECT
)
from django.utils.translation import gettext_lazy as _

from core.models import Reference


APP_NAME = "listings"


class ObjectType(Reference):
    """
    Different listing types (rooms, apartments, huts etc.)
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
