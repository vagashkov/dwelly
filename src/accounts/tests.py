from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import Account
from tests.user_data import good_account, good_profile

email = good_account.get(Account.Field.email)
password = good_account.get(Account.Field.password)
image_path = "{}/tests/user_photo.jpg".format(settings.BASE_DIR)


def create_good_account() -> Account:
    # create new account
    account = Account.objects.create_user(
        email=email,
        password=password
    )
    return account


class AccountTest(TestCase):
    """
    Manages account and profile data compliance tests
    """

    def test_create_standard_user(self):
        """
        Standard user creation test (with profile)
        :return:
        """

        # create new account and check it's privileges
        account = create_good_account()
        self.assertTrue(account.is_active)
        self.assertFalse(account.is_staff)
        self.assertFalse(account.is_superuser)

        # check if new profile was created
        profile = account.profile
        self.assertIsNotNone(profile)

        # fill profile with test data
        for key in good_profile.keys():
            profile.__setattr__(
                key,
                good_profile.get(key)
            )

        # check if profile was filled correctly
        for key in good_profile.keys():
            self.assertEqual(
                profile.__getattribute__(key),
                good_profile.get(key)
            )

        # finally check profile photo field
        profile.photo = SimpleUploadedFile(
            name="profile_photo.jpg",
            content=open(image_path, 'rb').read(),
            content_type="image/jpeg"
        )
        self.assertIsNotNone(profile.photo)

    def test_bad_country(self):
        # create new account
        account = create_good_account()
        try:
            account.profile.country = "ZZ"
        except TypeError:
            self.assertRaises(TypeError)

    def test_bad_language(self):
        # create new account
        account = create_good_account()
        try:
            account.profile.language = "zz"
        except TypeError:
            self.assertRaises(TypeError)

    def test_bad_phone(self):
        # create new account
        account = create_good_account()
        try:
            account.profile.phone = "zz"
        except TypeError:
            self.assertRaises(TypeError)

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
        Superuser (aka admin) creation test
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

    def test_signup_by_email(self):
        """
        Test if user can be created using email and password only
        :return:
        """
        Account.objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(Account.objects.all().count(), 1)
        self.assertEqual(
            Account.objects.all()[0].email,
            email
        )

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
        self.assertContains(self.response, "Login")
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
