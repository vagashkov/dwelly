from django.db.utils import IntegrityError
from django.test import TestCase
from django.urls import reverse

from .models import Account

from tests.data import good_account

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


class SignUpPage(TestCase):
    """
    Test user signup process
    """

    def test_signup_page(self):
        """
        Test user signup form existence
        :return:
        """
        self.response = self.client.get(
            reverse("account_signup")
        )
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "account/signup.html")
        self.assertContains(self.response, "Sign Up")
        self.assertNotContains(self.response, "Some wrong text")


class LoginPage(TestCase):
    """
    Test user login process
    """

    def setUp(self):
        Account.objects.create_user(
            email=email,
            password=password
            )

    def test_login_page(self):
        """
        Test login page existence
        :return:
        """

        self.response = self.client.get(
            reverse("account_login")
        )

        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "account/login.html")
        self.assertContains(self.response, "Sign In")
        self.assertNotContains(self.response, "Some wrong text")

    def test_login_process(self):
        """
        Test user login process
        :return:
        """

        self.response = self.client.post(
            reverse("account_login"),
            {
                "login": email,
                "password": password
            }
        )

        # after successful authorization user
        # should be redirected to the home page
        self.assertEqual(self.response.status_code, 302)
        self.assertEqual(
            self.response.headers.get("Location"),
            reverse("home")
        )

    def test_logout_process(self):
        """
        Test user logout process
        :return:
        """

        self.response = self.client.get(
            reverse("account_logout")
        )

        # after successful logout  user
        # should be redirected to the home page
        self.assertEqual(self.response.status_code, 302)
        self.assertEqual(
            self.response.headers.get("Location"),
            reverse("home")
        )
