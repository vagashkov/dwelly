from json import load
from json.decoder import JSONDecodeError
from os.path import exists

from django.conf import settings
from django.core.management import BaseCommand

from core.models import BaseStatus

from ...constants import (
    ERROR_MSG_NO_FIXTURE, ERROR_MSG_JSON_DECODING,
    INFO_MSG_RESERVATION_STATUSES_LOADED
)
from ...models import ReservationStatus
from ...urls import app_name


class Command(BaseCommand):
    """
    Loads default reservation statuses structure
    """

    def handle(self, *args, **options):
        """
        Command entry point
        :param args:
        :param options:
        :return:
        """

        # First we need to check if statuses file exists
        data_file = (
                settings.BASE_DIR /
                app_name /
                "defaults" /
                "reservation_statuses.json"
        )
        if not exists(data_file):
            self.stdout.write(
                ERROR_MSG_NO_FIXTURE.format(
                    "listings.fixtures.reservation_statuses.json"
                )
            )
            return

        with open(data_file) as source:
            try:
                statuses = load(source)
            except JSONDecodeError as e:
                self.stdout.write(
                    ERROR_MSG_JSON_DECODING.format(e)
                )
                return

            # First we need to create status objects
            for status in statuses:
                try:
                    status_object = ReservationStatus.objects.get_by_name(
                        status.get(BaseStatus.Field.name)
                    )
                except ReservationStatus.DoesNotExist:
                    status_object = ReservationStatus.objects.create(
                        name=status.get(BaseStatus.Field.name),
                        description=status.get(BaseStatus.Field.description),
                        is_initial=status.get(BaseStatus.Field.is_initial)
                    )
                    status_object.save()
                status["instance"] = status_object

            # Then - to establish connections between them
            for status in statuses:
                for predecessor in status.get(
                    BaseStatus.Field.previous_statuses
                ):
                    status["instance"].previous_statuses.add(
                        ReservationStatus.objects.get_by_name(
                            predecessor
                            )
                        )
                for successor in status.get(
                    BaseStatus.Field.next_statuses
                ):
                    status["instance"].next_statuses.add(
                        ReservationStatus.objects.get_by_name(
                            successor
                            )
                        )

        # Everything went just fine - let's inform user
        self.stdout.write(
            self.style.SUCCESS(
                INFO_MSG_RESERVATION_STATUSES_LOADED
            )
        )
