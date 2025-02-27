# Generated by Django 5.1.5 on 2025-02-27 13:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0004_listing_bathrooms_listing_bedrooms_listing_beds_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='check_in_time',
            field=models.TimeField(null=True, verbose_name='Check-in time'),
        ),
        migrations.AddField(
            model_name='listing',
            name='check_out_time',
            field=models.TimeField(null=True, verbose_name='Check-out time'),
        ),
        migrations.AddField(
            model_name='listing',
            name='hosts',
            field=models.ManyToManyField(related_name='listings', to=settings.AUTH_USER_MODEL, verbose_name='Hosts'),
        ),
        migrations.AddField(
            model_name='listing',
            name='instant_booking',
            field=models.BooleanField(default=False, verbose_name='Instant booking'),
        ),
    ]
