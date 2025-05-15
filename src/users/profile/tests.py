from os import mkdir
from os.path import exists
from shutil import rmtree

from PIL import Image

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from tests.test_data import create_good_user, good_profile

from ..models import Profile
from ..tests import email

TEST_DIR = settings.BASE_DIR / "test_data"


class ProfileTest(TestCase):
    """
    Test user signup process
    """

    def upload_photo(self, profile: Profile) -> None:
        # prepare test image to upload
        image = Image.new(
            "RGB",
            size=(2000, 2000),
            color=(155, 0, 0)
        )

        if not exists(TEST_DIR):
            mkdir(TEST_DIR)

        image_path = TEST_DIR / "test_photo.jpg"
        image.save(image_path)

        # "upload" profile photo
        with open(image_path, "rb") as profile_photo:
            profile.photo = SimpleUploadedFile(
                name="profile_photo.jpg",
                content=profile_photo.read(),
                content_type="image/jpeg"
            )

    def tearDown(self) -> None:
        # Cleaning temporary data
        try:
            rmtree(TEST_DIR)
        except OSError:
            pass

    def test_profile_creation(self) -> None:
        """
        Check user profile data
        :return:
        """
        profile = create_good_user().profile

        # check if new profile was created
        self.assertIsNotNone(profile)

    def test_fill_profile_data(self) -> None:
        """
        Check user profile data
        :return:
        """
        profile = create_good_user().profile

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

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def test_fill_profile_photo(self) -> None:
        """
        Check user profile photo
        :return:
        """

        profile = create_good_user().profile
        self.upload_photo(profile)
        profile.save()

        self.assertIsNotNone(profile.photo)

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def test_display_profile(self) -> None:
        """
        Test user profile page display option
        :return:
        """

        profile = create_good_user().profile

        # fill profile with test data
        for key in good_profile.keys():
            profile.__setattr__(
                key,
                good_profile.get(key)
                )
        self.upload_photo(profile)
        profile.save()

        # login using created account credentials
        self.client.force_login(profile.user)

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
        self.assertContains(
            self.response,
            "profile_photo"
        )
        self.assertNotContains(self.response, "Some wrong text")
