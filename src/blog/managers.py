from django.db.models import (
    Manager, QuerySet, Q
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

    def search_posts(self, query) -> QuerySet:
        return super().get_queryset().filter(
            Q(title__icontains=query)
            |
            Q(excerpt=query)
            |
            Q(text__icontains=query)
        ).filter(
            Q(status__name=ACTIVE_POST_STATUS)
        ).order_by(
            POSTS_ORDERING
        )
