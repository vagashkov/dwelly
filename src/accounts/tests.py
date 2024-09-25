from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

CustomUser = get_user_model()


class SignUpPageTests(TestCase):
    """
    Test user signup process
    """

    username = "newuser"
    email = "newuser@email.com"

    def setUp(self):
        url = reverse("account_signup")
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "account/signup.html")
        self.assertContains(self.response, "Sign Up")
        self.assertNotContains(self.response, "Some wrong text")

    def test_signup_form(self):
        get_user_model().objects.create_user(self.username, self.email)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(
            get_user_model().objects.all()[0].username,
            self.username
        )
        self.assertEqual(get_user_model().objects.all()[0].email, self.email)
