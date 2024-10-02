from django.test import TestCase
from django.urls import reverse

from .models import Account

email = "newuser@email.com"
password = "S0meStr0ngPaSSw0rd"


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
