from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Account, Profile


@receiver(post_save, sender=Account)
def build_profile_on_user_creation(sender, instance, created, **kwargs):
    """
    Generating an empty user profile on account creation
    """

    if created:
        profile = Profile(account=instance)
        profile.save()
