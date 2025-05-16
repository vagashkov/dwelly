from django.urls import path

from .views import Posts, PostDetails

app_name = "blog"

urlpatterns = [
    # API urls
    # path("api/", include("blog.data_api.urls")),
    # single post
    path("<slug:slug>", PostDetails.as_view(), name="post_details"),
    # all posts
    path("", Posts.as_view(), name="posts"),
]
