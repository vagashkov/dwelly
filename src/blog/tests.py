from os import mkdir
from os.path import exists
from shutil import rmtree

from PIL import Image

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from tests.test_data import create_good_user

from .models import Tag, Status, Post, Comment

TEST_DIR = settings.BASE_DIR / "test_data"


class BaseTest(TestCase):
    """
    Base test class for post-related testing
    """

    def upload_cover(self, post: Post) -> None:
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

        # "upload" post cover
        with open(image_path, "rb") as profile_photo:
            post.cover = SimpleUploadedFile(
                name="post_cover.jpg",
                content=profile_photo.read(),
                content_type="image/jpeg"
            )

    def tearDown(self) -> None:
        # Cleaning temporary data
        try:
            rmtree(TEST_DIR)
        except OSError:
            pass


class PostTests(BaseTest):
    """
    Testing single post object lifecycle
    """

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def setUp(self) -> None:
        """
        Prepare test data
        :return:
        """
        self.author = create_good_user()

        self.tag = Tag.objects.create(
            name="Test tag",
            description="Some test tag"
        )
        self.status = Status.objects.create(
            name="Draft"
        )
        self.post = Post.objects.create(
            title="Test post",
            excerpt="Test excerpt",
            author=self.author,
            text="Some test post content",
            slug="test-post",
            status=self.status
        )
        self.post.tags.set([self.tag])
        self.upload_cover(self.post)
        self.post.save()
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.author,
            text="Comment content"
        )

    def test_posts_list(self) -> None:
        response = self.client.get(reverse("blog:posts"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test post")
        self.assertContains(response, "Test excerpt")
        self.assertTemplateUsed(response, "blog/posts.html")

    def test_search_posts(self) -> None:
        response = self.client.get(
            reverse(
                "blog:search",
                query={
                    "q": "Test post"
                }
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test post")
        self.assertContains(response, "Test excerpt")
        self.assertTemplateUsed(response, "blog/posts.html")

    def test_unknown_post_details(self) -> None:
        no_response = self.client.get("/blog/no-post")
        self.assertEqual(no_response.status_code, 404)

    def test_existing_post_details(self) -> None:
        response = self.client.get(self.post.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test post")
        self.assertTemplateUsed(response, "blog/post_details.html")
        # Checking post data
        self.assertContains(response, self.author.email)
        self.assertContains(response, self.tag.name)
        self.assertContains(response, "Test post")
        self.assertContains(response, "Some test post content")
        self.assertContains(
            response,
            "post_cover_{}x{}.{}".format(
                settings.IMAGE_SIZE_MEDIUM[0],
                settings.IMAGE_SIZE_MEDIUM[1],
                settings.IMAGE_FORMAT
                )
        )
        # Checking comments section
        self.assertContains(response, "Comment content")
