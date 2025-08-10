from django.db.models import (
    Manager, QuerySet
)

from .constants import (
    ACTIVE_POST_STATUS, POSTS_ORDERING
)


class PostManager(Manager):
    """

    """

    def get_active_posts(self) -> QuerySet:
        """

        :return:
        """
        return super().get_queryset().filter(
            status__name=ACTIVE_POST_STATUS
        ).order_by(
            POSTS_ORDERING
        )
