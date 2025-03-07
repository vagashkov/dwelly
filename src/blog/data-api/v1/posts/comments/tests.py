from django.shortcuts import reverse

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY
)
from rest_framework.test import APITestCase

from .....models import Status, Postable, Post, Comment

from accounts.models import Account
from tests.data import good_account

email = good_account.get(Account.Field.email)
password = good_account.get(Account.Field.password)


class Tests(APITestCase):
    """
    Manages post comments testing
    """

    def setUp(self) -> None:
        """
        Pre-create some posts to browse
        :return:
        """
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

        # Create post
        self.post = Post.objects.create(
            title="Test post",
            author=self.admin_user,
            excerpt="Post excerpt",
            text="Post test",
            status=self.initial_status
        )

        self.first_comment = Comment(
            post=self.post,
            text="First comment text",
            author=self.standard_user
        )
        self.first_comment.save()

        self.second_comment = Comment(
            post=self.post,
            text="Second comment text",
            author=self.standard_user
        )
        self.second_comment.save()

    def test_get_non_existing_post_comments(self):
        """
        Tests non existing post comments display routine
        :return:
        """

        response = self.client.get(
            reverse(
                "blog_api_post_comments",
                kwargs={
                    Post.Field.slug: "abracadabra"
                }
            ),
        )

        self.assertEqual(
            response.status_code,
            HTTP_404_NOT_FOUND
        )

    def test_get_post_comments(self):
        """
        Tests existing post comments display routine
        :return:
        """

        response = self.client.get(
            reverse(
                "blog_api_post_comments",
                kwargs={
                    Post.Field.slug: self.post.slug
                }
            ),
        )

        self.assertEqual(
            response.status_code,
            HTTP_200_OK
        )

        self.assertEqual(
            len(response.data),
            2
        )

    def test_comment_non_auth_user(self):
        """
        Tests non existing post comment create routine
        :return:
        """

        response = self.client.post(
            reverse(
                "blog_api_post_comments",
                kwargs={
                    Post.Field.slug: self.post.slug
                }
            ),
            {
                Postable.Field.text: "Some comment"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            HTTP_403_FORBIDDEN
        )

    def test_comment_non_existing_post(self):
        """
        Tests non existing post comment create routine
        :return:
        """

        self.client.force_login(self.standard_user)

        response = self.client.post(
            reverse(
                "blog_api_post_comments",
                kwargs={
                    Post.Field.slug: "abracadabra"
                }
            ),
            {
                Postable.Field.text: "Some comment"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            HTTP_404_NOT_FOUND
        )

    def test_comment_post_invalid_data(self):
        """
        Tests for invalid data post comment
        :return:
        """

        self.client.force_login(self.standard_user)

        response = self.client.post(
            reverse(
                "blog_api_post_comments",
                kwargs={
                    Post.Field.slug: self.post.slug

                }
            ),
            {
                Postable.Field.text: 1
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            HTTP_422_UNPROCESSABLE_ENTITY
        )

    def test_comment_post(self):
        """
        Tests for post comment create routine
        :return:
        """

        self.client.force_login(self.standard_user)

        response = self.client.post(
            reverse(
                "blog_api_post_comments",
                kwargs={
                    Post.Field.slug: self.post.slug

                }
            ),
            {
                Postable.Field.text: "Test comment text"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            HTTP_201_CREATED
        )
