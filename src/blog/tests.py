from django.test import TestCase
from django.urls import reverse

from tests.test_data import create_good_user

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

    def test_posts_list(self) -> None:
        response = self.client.get(reverse("blog:posts"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test post")
        self.assertTemplateUsed(response, "blog/posts.html")

    def test_unknown_post_details(self) -> None:
        no_response = self.client.get("/blog/no-post")
        self.assertEqual(no_response.status_code, 404)

    def test_existing_post_details(self) -> None:
        response = self.client.get(self.post.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test post")
        self.assertTemplateUsed(response, "blog/post_details.html")
