import time
from psycopg import OperationalError as PsycopgOpError

from django.core.management import BaseCommand
from django.db.utils import OperationalError

from ...constants import (
    MSG_DB_AVAILABLE, MSG_DB_NOT_AVAILABLE
)


class Command(BaseCommand):
    """
    Django vs database launch synchronizer
    """

    # Time in second between tryouts
    SLEEP_INTERVAL = 1

    def handle(self, *args, **options):
        """
        Command entry point
        :param args:
        :param options:
        :return:
        """

        self.stdout.write("Waiting for database")
        db_up = False

        # Trying to connect to database every 1 second
        while not db_up:
            try:
                # Connection established
                self.check(
                    databases=["default"]
                )
                db_up = True
            # Database is still not ready
            except (PsycopgOpError, OperationalError):
                self.stdout.write(
                    MSG_DB_NOT_AVAILABLE.format(
                        self.SLEEP_INTERVAL
                    )
                )
                time.sleep(self.SLEEP_INTERVAL)

        self.stdout.write(
            self.style.SUCCESS(MSG_DB_AVAILABLE)
        )
