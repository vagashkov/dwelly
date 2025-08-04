from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def build_profile_on_user_creation(
        sender: User,
        instance: User,
        created: bool,
        **kwargs: dict
) -> None:
    """
    Generating an empty user profile on new user creation
    """

    if created:
        profile = Profile(user=instance)
        profile.save()
