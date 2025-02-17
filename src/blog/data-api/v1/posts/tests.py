import io
from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import reverse

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    HTTP_422_UNPROCESSABLE_ENTITY
)
from rest_framework.test import APITestCase

from accounts.models import Account
from tests.data import good_account

from ....models import Tag, Status, Postable, Post

email = good_account.get(Account.Field.email)
password = good_account.get(Account.Field.password)
mandatory_fields = [
    Post.Field.title,
    Post.Field.excerpt,
    Postable.Field.text
]
fields = [
    Post.Field.title,
    Post.Field.excerpt,
    Postable.Field.author,
    Post.Field.cover,
    Post.Field.tags,
]
list_fields = fields.copy().append(Post.Field.slug)
details_fields = fields.copy().append(Postable.Field.text)

post_data = {
    Post.Field.title: "Test title",
    Post.Field.excerpt: "Test excerpt",
    Postable.Field.text: "Some test text",
}


class Posts(APITestCase):
    """
    Test posts browsing scenarios
    """

    def setUp(self) -> None:
        """
        Pre-create some posts to browse
        :return:
        """
        self.first_tag = Tag.objects.create(
            name="FirstTag"
        )

        self.second_tag = Tag.objects.create(
            name="SecondTag"
        )

        self.standard_user = Account.objects.create(
            email=email,
            password=password
        )

        self.admin_user = Account.objects.create_superuser(
            email="admin{}".format(email),
            password=password
        )

        self.initial_status = Status.objects.create(
            name="Draft",
            is_initial=True
        )

        # Create first post
        self.first_post = Post.objects.create(
            title="First",
            author=self.admin_user,
            excerpt="First post excerpt",
            text="First post excerpt",
            status=self.initial_status
        )
        self.first_post.tags.add(
            self.first_tag,
            self.second_tag
        )
        # Create first post cover
        img_content = io.BytesIO()
        image = Image.new("RGB", size=(800, 600), color=(155, 0, 0))
        image.save(img_content, "JPEG")
        self.first_post.cover = SimpleUploadedFile(
            name="first_post_cover.jpeg",
            content=img_content.getvalue(),
            content_type="image/jpeg"
        )
        img_content.flush()

        # Create seconf post
        second_post = Post.objects.create(
            title="Second",
            author=self.admin_user,
            excerpt="First post excerpt",
            text="First post excerpt",
            status=self.initial_status
        )
        second_post.tags.add(self.first_tag)

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

    def test_create_no_auth(self):
        # Check if new post can be created w/o authentication
        response = self.client.post(
            reverse("blog_api_posts"),
            {},
            format="json"
        )
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_create_standard_user(self):
        # Check if new post can be created by standard user
        self.client.force_login(self.standard_user)

        response = self.client.post(
            reverse("blog_api_posts"),
            {},
            format="json"
        )
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_create_no_mandatory_field(self):
        # Check if new post can be created w/o mandatory fields
        self.client.force_login(self.admin_user)

        for field in mandatory_fields:
            bad_data = post_data.copy()
            del bad_data[field]
            response = self.client.post(
                reverse("blog_api_posts"),
                bad_data,
                format="json"
                )
            self.assertEqual(
                response.status_code,
                HTTP_422_UNPROCESSABLE_ENTITY
                )

    def test_create_post(self):
        # Check if new post can be created with mandatory fields
        self.client.force_login(self.admin_user)

        # Getting tag data
        tags = [
            tag.id for tag in Tag.objects.all()[:2]
        ]
        post_data[Post.Field.tags] = tags

        response = self.client.post(
            reverse("blog_api_posts"),
            post_data,
            format="json"
            )
        self.assertEqual(
            response.status_code,
            HTTP_201_CREATED
            )

    def test_create_post_cover_no_image(self):
        # Checking post cover upload routine
        # without cover attached

        self.client.force_login(self.admin_user)

        response = self.client.post(
            reverse(
                "blog_api_post_cover",
                kwargs={
                    Post.Field.slug: self.first_post.slug
                }
            )
        )

        self.assertEqual(
            response.status_code,
            HTTP_422_UNPROCESSABLE_ENTITY
        )

    def test_create_unknown_post_cover(self):
        # Checking post cover upload routine
        # for non-existing post

        # Create post cover
        img_content = io.BytesIO()
        image = Image.new("RGB", size=(800, 600), color=(0, 155, 0))
        image.save(img_content, "JPEG")
        img_content.name = "cover.jpg"
        img_content.seek(0)

        # Trying to upload post cover
        self.client.force_login(self.admin_user)
        response = self.client.post(
            reverse(
                "blog_api_post_cover",
                kwargs={
                    Post.Field.slug: "abracadabra"
                }
            ),
            {
                Post.Field.cover: img_content
            },
            format="multipart"
        )
        img_content.flush()

        # Time to evaluate result
        self.assertEqual(
            response.status_code,
            HTTP_404_NOT_FOUND
        )

    def test_create_post_non_image_cover(self):
        # Checking post cover upload routine
        # for upsupported image format

        # Create post cover
        img_content = io.BytesIO(b"Definitely not an image!")
        img_content.name = "cover.jpg"
        img_content.seek(0)

        # Trying to upload post cover
        self.client.force_login(self.admin_user)
        response = self.client.post(
            reverse(
                "blog_api_post_cover",
                kwargs={
                    Post.Field.slug: self.first_post.slug
                }
            ),
            {
                Post.Field.cover: img_content
            },
            format="multipart"
        )
        img_content.flush()

        # Time to evaluate result
        self.assertEqual(
            response.status_code,
            HTTP_415_UNSUPPORTED_MEDIA_TYPE
        )

    def test_create_post_cover(self):
        # Checking post cover upload routine

        # Create post cover
        img_content = io.BytesIO()
        image = Image.new("RGB", size=(800, 600), color=(0, 155, 0))
        image.save(img_content, "JPEG")
        img_content.name = "cover.jpg"
        img_content.seek(0)

        # Trying to upload post cover
        self.client.force_login(self.admin_user)
        response = self.client.post(
            reverse(
                "blog_api_post_cover",
                kwargs={
                    Post.Field.slug: self.first_post.slug
                }
            ),
            {
                Post.Field.cover: img_content
            },
            format="multipart"
        )
        img_content.flush()

        # Time to evaluate result
        self.assertEqual(
            response.status_code,
            HTTP_202_ACCEPTED
        )
