import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import (
    Model, BigAutoField, UUIDField,
    CharField, DateTimeField, BooleanField,
    ManyToManyField
)
from django.utils.translation import gettext_lazy as _

from .constants import MSG_INITIAL_STATUS_PREDECESSORS


class BaseModel(Model):
    """
    Base model class containing standard
    (common for all entities) attributes only
    """

    class Meta:
        abstract = True

    class Field:
        id: str = "id"
        uuid: str = "uuid"
        public_id: str = "public_id"
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

    def _get_public_id(self) -> str:
        """
        Calculates public_id based on model instance id
        :return:
        """
        return settings.FF3_CIPHER.encrypt(
            str(self.id).zfill(
                settings.FF3_LENGTH
            )
        )

    public_id = property(_get_public_id)

    created_at: DateTimeField = DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at")

    )

    updated_at: DateTimeField = DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at")
    )


class Reference(BaseModel):
    """
    References base class
    """

    class Field:
        name: str = "name"
        description: str = "description"

    class Meta:
        abstract = True

    name: str = CharField(
        null=False,
        blank=False,
        unique=True,
        max_length=64,
        verbose_name=_("Name")
    )

    description: str = CharField(
        null=False,
        blank=True,
        default="",
        max_length=256,
        verbose_name=_("Description")
    )

    def __str__(self) -> str:
        return "{}".format(self.name)

    def natural_key(self) -> tuple[str]:
        return (self.name,)


class BaseStatus(Reference):
    """
    Blog post statuses
    """
    class Meta:
        abstract = True
        verbose_name_plural = "statuses"

    class Field:
        name: str = "name"
        description: str = "description"
        is_initial: str = "is_initial"
        previous_statuses: str = "previous_statuses"
        next_statuses: str = "next_statuses"

    is_initial: BooleanField = BooleanField(
        null=False,
        blank=True,
        default=False
    )

    previous_statuses = ManyToManyField(
        "self",
        blank=True,
        symmetrical=False,
        related_name="successors",
        verbose_name=_("Previous statuses")
    )

    next_statuses = ManyToManyField(
        "self",
        blank=True,
        symmetrical=False,
        related_name="predecessors",
        verbose_name=_("Next statuses")
    )

    def clean(self):
        """
        Some pre-save data validations
        :return:
        """

        if self.is_initial and self.previous_statuses.count():
            raise ValidationError(
                MSG_INITIAL_STATUS_PREDECESSORS
            )
