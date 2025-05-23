import io
from PIL import Image

from django.conf import settings
from django.shortcuts import reverse

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_204_NO_CONTENT,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    HTTP_422_UNPROCESSABLE_ENTITY
)
from rest_framework.test import override_settings

from users.models import User
from tests.test_data import good_user

from ....models import Tag, Status, Postable, Post
from ....tests import BaseTest

TEST_DIR = settings.BASE_DIR / "test_data"

email = good_user.get(User.Field.email)
password = good_user.get(User.Field.password)
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
    Post.Field.title: "Test",
    Post.Field.excerpt: "Test",
    Postable.Field.text: "Some",
}


class Posts(BaseTest):
    """
    Test posts browsing scenarios
    """

    @override_settings(MEDIA_ROOT=TEST_DIR)
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

        self.standard_user = User.objects.create(
            email=email,
            password=password
        )

        self.admin_user = User.objects.create_superuser(
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
        # Upload first post cover
        self.upload_cover(self.first_post)
        self.first_post.save()

        # Create second post
        self.second_post = Post.objects.create(
            title="Second",
            author=self.admin_user,
            excerpt="First post excerpt",
            text="First post excerpt",
            status=self.initial_status
        )
        self.second_post.tags.add(self.first_tag)

        # Create second post cover
        self.upload_cover(self.second_post)
        self.second_post.save()

    def test_posts_list(self) -> None:
        response = self.client.get(
            reverse("blog:api_posts"),
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

    def test_post_details(self) -> None:
        response = self.client.get(
            reverse(
                "blog:api_post_details",
                kwargs={
                    Post.Field.slug: self.first_post.slug
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

    def test_create_no_auth(self) -> None:
        # Check if new post can be created w/o authentication
        response = self.client.post(
            reverse("blog:api_posts"),
            {},
            format="json"
        )
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_create_standard_user(self) -> None:
        # Check if new post can be created by standard user
        self.client.force_login(self.standard_user)

        response = self.client.post(
            reverse("blog:api_posts"),
            {},
            format="json"
        )
        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_create_no_mandatory_field(self) -> None:
        # Check if new post can be created w/o mandatory fields
        self.client.force_login(self.admin_user)

        for field in mandatory_fields:
            bad_data = post_data.copy()
            del bad_data[field]
            response = self.client.post(
                reverse("blog:api_posts"),
                bad_data,
                format="json"
                )
            self.assertEqual(
                response.status_code,
                HTTP_422_UNPROCESSABLE_ENTITY
                )

    def test_create_post(self) -> None:
        # Check if new post can be created with mandatory fields
        self.client.force_login(self.admin_user)

        # Getting tag data
        tags = [
            tag.id for tag in Tag.objects.all()[:2]
        ]
        post_data[Post.Field.tags] = tags

        response = self.client.post(
            reverse("blog:api_posts"),
            post_data,
            format="json"
            )
        self.assertEqual(
            response.status_code,
            HTTP_201_CREATED
            )

    def test_create_post_cover_no_image(self) -> None:
        # Checking post cover upload routine
        # without cover attached

        self.client.force_login(self.admin_user)

        response = self.client.post(
            reverse(
                "blog:api_post_cover",
                kwargs={
                    Post.Field.slug: self.first_post.slug
                }
            )
        )

        self.assertEqual(
            response.status_code,
            HTTP_422_UNPROCESSABLE_ENTITY
        )

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def test_create_unknown_post_cover(self) -> None:
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
                "blog:api_post_cover",
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

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def test_create_post_non_image_cover(self) -> None:
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
                "blog:api_post_cover",
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

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def test_create_post_cover(self) -> None:
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
                "blog:api_post_cover",
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

    def test_get_post_cover(self) -> None:
        response = self.client.get(
            reverse(
                "blog:api_post_cover",
                kwargs={
                    Post.Field.slug: self.first_post.slug
                }
            ),
        )

        # Check results through response code
        self.assertEqual(
            response.status_code,
            HTTP_200_OK
        )

        # Check received data
        self.assertIn(
            Post.Field.cover,
            response.data
            )

    def test_delete_post_cover(self) -> None:
        # Checking post cover delete routine

        # Trying to upload post cover
        self.client.force_login(self.admin_user)
        response = self.client.delete(
            reverse(
                "blog:api_post_cover",
                kwargs={
                    Post.Field.slug: self.first_post.slug
                }
            ),
        )

        # Time to evaluate result
        self.assertEqual(
            response.status_code,
            HTTP_204_NO_CONTENT
        )
