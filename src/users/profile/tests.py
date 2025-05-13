from shutil import rmtree

from PIL import Image

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from ..models import User, Profile
from ..tests import email, password, good_profile

TEST_DIR = settings.BASE_DIR / "test_data"


class ProfileTest(TestCase):
    """
    Test user signup process
    """

    def create_good_user(self) -> User:
        # create new user
        user = User.objects.create_user(
            email=email,
            password=password
        )
        return user

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def setUp(self) -> None:
        # create user and related profile objects
        self.profile: Profile = self.create_good_user().profile

        # fill profile with test data
        for key in good_profile.keys():
            self.profile.__setattr__(
                key,
                good_profile.get(key)
            )
        # finally check profile photo field
        image = Image.new(
            "RGB",
            size=(2000, 2000),
            color=(155, 0, 0)
        )

        # finally check profile photo field
        self.profile.photo = SimpleUploadedFile(
            name="profile_photo.jpg",
            content=image.tobytes(),
            content_type="image/jpeg"
        )
        self.profile.save()

        # login using created account credentials
        self.client.force_login(self.profile.user)

    def tearDown(self) -> None:
        # Cleaning temporary data
        try:
            rmtree(TEST_DIR)
        except OSError:
            pass

    def test_display_profile(self) -> None:
        """
        Test user profile page display option
        :return:
        """

        self.response = self.client.get(
            reverse("user_display_profile")
        )
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "users/display_profile.html")

        # checking text data
        self.assertContains(
            self.response,
            email
        )
        for key in good_profile:
            self.assertContains(
                self.response,
                good_profile.get(key)
            )
        # checking photo
        self.assertContains(
            self.response,
            "profile_photo.jpg"
        )
        self.assertNotContains(self.response, "Some wrong text")
