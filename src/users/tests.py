from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.utils import IntegrityError
from django.test import TestCase
from django.urls import reverse

from .models import User, Profile

good_user = {
    User.Field.email: "test@email.com",
    User.Field.password: "S0meStr0ngPaSSw0rd",
}

good_profile = {
    Profile.Field.first_name: "Some",
    Profile.Field.last_name: "User",
    Profile.Field.phone: "+302374071345",
    Profile.Field.bio: "Some test user"
}

email = good_user.get(User.Field.email)
password = good_user.get(User.Field.password)


class UserTest(TestCase):
    """
    Manages user and profile data compliance tests
    """

    def create_good_user(self) -> User:
        # create new user
        return User.objects.create_user(
            email=email,
            password=password
        )

    def test_create_user_no_email(self) -> None:
        """
        Test if user user can be created with empty email
        :return:
        """
        try:
            User.objects.create_user(
                email="",
                password=password
            )
        except ValueError:
            self.assertRaises(ValueError)

    def test_create_user_no_password(self) -> None:
        """
        Test if user user can be created with empty password
        :return:
        """
        try:
            User.objects.create_user(
                email=email,
                password=""
            )
        except ValueError:
            self.assertRaises(ValueError)

    def test_create_standard_user(self) -> None:
        """
        Create new user with all data needed
        :return:
        """
        user = self.create_good_user()
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertIsNotNone(user.public_id)

    def test_user_profile(self) -> None:
        """
        Check user profile data
        :return:
        """
        profile = self.create_good_user().profile

        # check if new profile was created
        self.assertIsNotNone(profile)

    def test_fill_profile_data(self) -> None:
        """
        Check user profile data
        :return:
        """
        profile = self.create_good_user().profile

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

    def test_fill_profile_photo(self) -> None:
        """
        Check user profile photo
        :return:
        """

        profile = self.create_good_user().profile

        image = Image.new(
            "RGB",
            size=(2000, 2000),
            color=(155, 0, 0)
        )

        # finally check profile photo field
        profile.photo = SimpleUploadedFile(
            name="profile_photo.jpg",
            content=image.tobytes(),
            content_type="image/jpeg"
        )
        self.assertIsNotNone(profile.photo)

    def test_bad_phone(self) -> None:
        # check phone format verification
        try:
            self.create_good_user().profile.phone = "zz"
        except TypeError:
            self.assertRaises(TypeError)

    def test_create_user_duplicate_email(self) -> None:
        """
        Check if user user can be created
        with duplicate email
        :return:
        """
        User.objects.create_user(
            email=email,
            password=password
        )
        try:
            User.objects.create_user(
                email=email,
                password=password
            )
        except IntegrityError:
            self.assertRaises(IntegrityError)

    def test_create_staff_user(self) -> None:
        """
        Test staff user creation
        :return:
        """
        user = User.objects.create_user(
            email=email,
            password=password,
            is_staff=True
        )
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self) -> None:
        """
        Test superuser (aka admin) creation
        :return:
        """

        user = User.objects.create_superuser(
            email=email,
            password=password
        )
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


class SignUpPage(TestCase):
    """
    Test user signup process
    """

    def test_signup_page(self) -> None:
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

    def setUp(self) -> None:
        User.objects.create_user(
            email=email,
            password=password
            )

    def test_login_page(self) -> None:
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

    def test_login_process(self) -> None:
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

    def test_logout_process(self) -> None:
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
