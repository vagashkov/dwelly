from json import load
from json.decoder import JSONDecodeError
from os.path import exists

from django.conf import settings
from django.core.management import BaseCommand

from core.models import Reference

from ...constants import (
    ERROR_MSG_NO_FIXTURE, ERROR_MSG_JSON_DECODING,
    INFO_MSG_AMENITIES_LOADED
)
from ...models import Category, Amenity
from ...urls import app_name


class Command(BaseCommand):
    """
    Loads default amenities list
    """

    def handle(self, *args, **options):
        """
        Command entry point
        :param args:
        :param options:
        :return:
        """

        # First we need to check if amenities file exists
        data_file = (
                settings.BASE_DIR /
                app_name /
                "defaults" /
                "amenities.json"
        )
        if not exists(data_file):
            self.stdout.write(
                ERROR_MSG_NO_FIXTURE.format(
                    "listings.fixtures.amenities.json"
                )
            )
            return

        with open(data_file) as source:
            try:
                categories = load(source)
            except JSONDecodeError as e:
                self.stdout.write(
                    ERROR_MSG_JSON_DECODING.format(e)
                )
                return

            # First we need to create or update categories objects
            for category in categories:
                try:
                    category_object = Category.objects.get(
                        name=category.get(Reference.Field.name)
                    )
                    category_object.description = category.get(
                        Reference.Field.description
                    )
                except Category.DoesNotExist:
                    category_object = Category.objects.create(
                        name=category.get(Reference.Field.name),
                        description=category.get(Reference.Field.description),
                    )
                category_object.save()
                category["instance"] = category_object

                # Then - to fill categories with amenities
                for amenity in category.get("amenities"):
                    try:
                        amenity_object = Amenity.objects.get(
                            name=amenity.get(Reference.Field.name)
                        )
                        amenity_object.description = amenity.get(
                            Reference.Field.description
                        )
                    except Amenity.DoesNotExist:
                        amenity_object = Amenity.objects.create(
                            name=amenity.get(Reference.Field.name),
                            description=amenity.get(
                                Reference.Field.description
                            ),
                            category=category.get("instance")
                        )
                    amenity_object.save()

        # Everything went just fine - let's inform user
        self.stdout.write(
            self.style.SUCCESS(
                INFO_MSG_AMENITIES_LOADED
            )
        )
