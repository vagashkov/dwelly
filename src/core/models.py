from django.db.models import (
    Model, BigAutoField, DateTimeField
)
from django.utils.translation import gettext_lazy as _


class BaseModel(Model):
    """
    Base model class containing standard
    (common for all entities) attributes only
    """

    class Meta:
        abstract = True

    class Field:
        id: str = "id"
        created_at: str = "created_at"
        updated_at: str = "updated_at"

    id: BigAutoField = BigAutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name=_("ID")
    )

    created_at: DateTimeField = DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at")

    )

    updated_at: DateTimeField = DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at")
    )
