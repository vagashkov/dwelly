from django.test import TestCase
from django.urls import reverse

from accounts.models import Account
from accounts.tests import good_account

from .models import Tag, Status, Post, Comment


class PostTests(TestCase):
    """
    Testing single post object lifecycle
    """

    def setUp(self) -> None:
        """
        Prepare test data
        :return:
        """
        self.author = Account.objects.create(
            email=good_account.get(
                Account.Field.email
            ),
            password=good_account.get(
                Account.Field.password
            )
        )

        self.tag = Tag.objects.create(
            name="Test tag",
            description="Some test tag"
        )
        self.status = Status.objects.create(
            name="Draft"
        )
        self.post = Post.objects.create(
            title="Test post",
            author=self.author,
            text="Some test post content",
            slug="test-post",
            status=self.status
        )
        self.post.tags.set([self.tag])
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.author,
            text="Comment content"
        )

    def test_posts_list(self):
        response = self.client.get(reverse("blog_home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test post")
        self.assertTemplateUsed(response, "blog/index.html")

    def test_unknown_post_details(self):
        no_response = self.client.get("/blog/no-post")
        self.assertEqual(no_response.status_code, 404)

    def test_existing_post_details(self):
        response = self.client.get(self.post.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test post")
        self.assertTemplateUsed(response, "blog/post_details.html")
