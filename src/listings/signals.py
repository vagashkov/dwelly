from django.db.models.signals import post_save
from django.dispatch import receiver

from core.utils.dates import daterange_generator

from .models import PriceTag, DayRate


@receiver(post_save, sender=PriceTag)
def price_tag_post_save_receiver(
        sender, instance, created, **kwargs
):
    # New PriceTag instance was created
    for current_date in daterange_generator(
            instance.start_date, instance.end_date
    ):
        # For each perspective day rate, first check if it already exists
        try:
            day_rate = DayRate.objects.get(
                listing=instance.listing,
                date=current_date,
            )
        # Not found - create
        except DayRate.DoesNotExist:
            DayRate.objects.create(
                listing=instance.listing,
                date=current_date,
                price_tag=instance,
                price=instance.price
            )
        else:
            # Found - check RateTags intersection
            if day_rate.price_tag != instance:
                raise ValueError(
                    "There is a day rate for date {}".format(
                        current_date
                    )
                )
            # Or update day rate if necessary
            else:
                if day_rate.price != instance.price:
                    day_rate.price = instance.price
                    day_rate.save()
