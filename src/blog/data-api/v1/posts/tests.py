import io
from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import reverse

from rest_framework.status import (
    HTTP_200_OK,
)
from rest_framework.test import APITestCase

from accounts.models import Account
from tests.data import good_account

from ....models import Tag, Status, Postable, Post

email = good_account.get(Account.Field.email)
password = good_account.get(Account.Field.password)
fields = [
    Post.Field.title,
    Postable.Field.author,
    Post.Field.excerpt,
    Post.Field.cover,
    Post.Field.tags,
]
list_fields = fields.copy().append(Post.Field.slug)
details_fields = fields.copy().append(Postable.Field.text)


class Posts(APITestCase):
    """
    Test posts browsing scenarios
    """

    def setUp(self) -> None:
        """
        Pre-create some posts to browse
        :return:
        """
        first_tag = Tag.objects.create(
            name="FirstTag"
        )
        second_tag = Tag.objects.create(
            name="SecondTag"
        )

        author = Account.objects.create(
            email=email,
            password=password
        )

        status = Status.objects.create(
            name="Draft"
        )

        # Create first post
        first_post = Post.objects.create(
            title="First",
            author=author,
            excerpt="First post excerpt",
            text="First post excerpt",
            status=status
        )
        first_post.tags.add(first_tag, second_tag)
        # Create first post cover
        img_content = io.BytesIO()
        image = Image.new("RGB", size=(800, 600), color=(155, 0, 0))
        image.save(img_content, "JPEG")
        first_post.cover = SimpleUploadedFile(
            name="first_post_cover.jpeg",
            content=img_content.getvalue(),
            content_type="image/jpeg"
        )
        img_content.flush()

        # Create seconf post
        second_post = Post.objects.create(
            title="Second",
            author=author,
            excerpt="First post excerpt",
            text="First post excerpt",
            status=status
        )
        second_post.tags.add(first_tag)

        # Create second post cover
        img_content = io.BytesIO()
        image = Image.new("RGB", size=(800, 600), color=(0, 155, 0))
        image.save(img_content, "JPEG")
        second_post.cover = SimpleUploadedFile(
            name="second_post_cover.jpeg",
            content=img_content.getvalue(),
            content_type="image/jpeg"
        )
        img_content.flush()

    def test_posts_list(self):
        response = self.client.get(
            reverse("blog_api_posts"),
        )

        # Check results through response code
        self.assertEqual(
            response.status_code,
            HTTP_200_OK
        )

        # Check received data
        # - data length
        self.assertEqual(
            len(response.data),
            2
        )
        # - data content
        for field in fields:
            self.assertIn(
                field,
                response.data[0]
                )

    def test_post_details(self):
        response = self.client.get(
            reverse(
                "blog_api_post_details",
                kwargs={
                    Post.Field.slug: Post.objects.all()[0].slug
                }
            ),
        )

        # Check results through response code
        self.assertEqual(
            response.status_code,
            HTTP_200_OK
        )

        # Check received data
        # - data content
        for field in fields:
            self.assertIn(
                field,
                response.data
                )
