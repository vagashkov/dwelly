import uuid

from django.db.models import (
    Model, BigAutoField, UUIDField, DateTimeField
)
from django.utils.translation import gettext_lazy as _


class BaseModel(Model):
    """
    Base model class containing standard attributes only
    """

    class Meta:
        abstract = True

    class Field:
        id: str = "id"
        uuid: str = "uuid"
        created_at: str = "created_at"
        updated_at: str = "updated_at"

    id: BigAutoField = BigAutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name=_("ID")
    )

    uuid: UUIDField = UUIDField(
        null=False,
        unique=True,
        editable=False,
        primary_key=False,
        auto_created=True,
        default=uuid.uuid4,
        verbose_name=_("UUID")
    )

    created_at: DateTimeField = DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at")

    )

    updated_at: DateTimeField = DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at")
    )
