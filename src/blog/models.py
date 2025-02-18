from django.contrib.auth import get_user_model
from django.db.models import (
    ForeignKey, PROTECT, CASCADE, ManyToManyField,
    BooleanField, CharField, TextField, SlugField,
    ImageField, PositiveSmallIntegerField
)
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel, Reference

APP_NAME = "blog"


def upload_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<post_uuid>/<filename>
    return "{}/{}/{}".format(
        APP_NAME,
        instance.uuid,
        filename
    )


class Tag(Reference):
    """
    Blog post tags
    """
    pass


class Status(Reference):
    """
    Blog post statuses
    """
    class Meta:
        verbose_name_plural = "statuses"

    class Field:
        name: str = "name"
        description: str = "description"
        is_initial: str = "is_initial"

    is_initial: BooleanField = BooleanField(
        null=False,
        blank=True,
        default=False
    )


class Postable(BaseModel):
    """
    Base class for both blog posts and comments
    """

    class Field:
        author: str = "author"
        text: str = "text"

    class Meta:
        abstract = True

    author: ForeignKey = ForeignKey(
        get_user_model(),
        null=False,
        blank=False,
        on_delete=PROTECT
    )

    text: TextField = TextField(
        null=False,
        blank=False
    )


class Post(Postable):
    """
    Blog post class
    """

    class Field:
        title: str = "title"
        excerpt: str = "excerpt"
        tags: str = "tags"
        cover: str = "cover"
        slug: str = "slug"
        status: str = "status"

    title: CharField = CharField(
        null=False,
        blank=False,
        max_length=64,
        verbose_name=_("Title")
    )

    excerpt: CharField = CharField(
        null=False,
        blank=False,
        max_length=256,
        verbose_name=_("Excerpt")
    )

    tags: ManyToManyField = ManyToManyField(
        Tag,
        related_name="posts",
        verbose_name=_("Tags")
    )

    cover: ImageField = ImageField(
        null=True,
        upload_to=upload_path,
        verbose_name=_("Cover")
    )

    slug: SlugField = SlugField(
        null=False,
        blank=True,
        unique=True,
        db_index=True,
        verbose_name=_("Slug")
    )

    status: ForeignKey = ForeignKey(
        Status,
        null=False,
        blank=False,
        related_name="posts",
        on_delete=PROTECT,
        verbose_name=_("Status")
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Performs additional object data manipulations
        :param args:
        :param kwargs:
        :return:
        """
        # create slug for reverse url
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("post_details", args=[self.slug])


class Comment(Postable):
    """
    Post comment class
    """

    class Field:
        post: str = "post"

    post = ForeignKey(
        Post,
        null=False,
        on_delete=CASCADE,
        related_name="comments"
    )


class Rating(BaseModel):
    """
    User's ratings for posts
    """

    class Fields:
        post: str = "post"
        author: str = "author"
        value: str = "value"

    post = ForeignKey(
        Post,
        null=False,
        on_delete=CASCADE,
        related_name="ratings"
    )

    author: ForeignKey = ForeignKey(
        get_user_model(),
        null=False,
        blank=False,
        related_name="ratings",
        on_delete=CASCADE,
        verbose_name=_("Author")
    )

    value: PositiveSmallIntegerField = PositiveSmallIntegerField(
        null=False,
        blank=False,
        default=0,
        verbose_name=_("Value")
    )
