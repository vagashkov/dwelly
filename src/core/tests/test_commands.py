from unittest.mock import patch
from psycopg import OperationalError as PsycopgOpError

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch("core.management.commands.wait_for_db.Command.check")
class CommandTest(SimpleTestCase):
    """
    Test management commands
    """

    def test_wait_for_db_command(self, patched_check) -> None:
        """
        Check if wait_for_db command is available and called
        :return:
        """

        patched_check.return_value = True

        # Perform management command call
        call_command("wait_for_db")

        # Check if check was really called
        patched_check.assert_called_once_with(
            databases=["default"]
        )

    @patch("time.sleep")
    def test_wait_for_db_delay(self, patched_sleep, patched_check) -> None:
        """
        Check if getting OperationalError will make Django to wait for db
        :param patched_check:
        :return:
        """

        # Typical PostgreSQL instance connection try-out results sequence
        # On 1st and 2nd database is still starting
        # On 3rd, 4th and 5th - started, but does not accept connections yet
        # On 6th - we finally connected successfully
        patched_check.side_effect = (
                [PsycopgOpError] * 2 + [OperationalError] * 3 + [True]
        )

        # Perform management command call
        call_command("wait_for_db")

        # Check if check was called correctly
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(
            databases=["default"]
        )
