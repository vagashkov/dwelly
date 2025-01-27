from django.test import TestCase

from django.db.utils import IntegrityError

from .models import Account

good_account = {
    Account.Field.email: "newuser@email.com",
    Account.Field.password: "S0meStr0ngPaSSw0rd",
}

email = good_account.get(Account.Field.email)
password = good_account.get(Account.Field.password)


class AccountTest(TestCase):
    """
    Manages account and profile data compliance tests
    """

    def test_create_account_no_email(self):
        """
        Test if user account can be created with empty email
        :return:
        """
        try:
            Account.objects.create_user(
                email="",
                password=password
            )
        except ValueError:
            self.assertRaises(ValueError)

    def test_create_account_no_password(self):
        """
        Test if user account can be created with empty password
        :return:
        """
        try:
            Account.objects.create_user(
                email=email,
                password=""
            )
        except ValueError:
            self.assertRaises(ValueError)

    def test_create_standard_account(self):
        """
        Create new account with all data needed
        :return:
        """
        account = Account.objects.create_user(
            email=email,
            password=password
        )
        self.assertTrue(account.is_active)
        self.assertFalse(account.is_staff)
        self.assertFalse(account.is_superuser)
        self.assertIsNotNone(account.public_id)

    def test_create_account_duplicate_email(self):
        """
        Check if user account can be created
        with duplicate email
        :return:
        """
        Account.objects.create_user(
            email=email,
            password=password
        )
        try:
            Account.objects.create_user(
                email=email,
                password=password
            )
        except IntegrityError:
            self.assertRaises(IntegrityError)

    def test_create_staff_user(self):
        """
        Test staff user creation
        :return:
        """
        account = Account.objects.create_user(
            email=email,
            password=password,
            is_staff=True
        )
        self.assertTrue(account.is_active)
        self.assertTrue(account.is_staff)
        self.assertFalse(account.is_superuser)

    def test_create_superuser(self):
        """
        Test superuser (aka admin) creation
        :return:
        """

        account = Account.objects.create_superuser(
            email=email,
            password=password
        )
        self.assertTrue(account.is_active)
        self.assertTrue(account.is_staff)
        self.assertTrue(account.is_superuser)
