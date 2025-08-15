from django.urls import path, include

from .views import Posts, Search, PostDetails

app_name = "blog"

urlpatterns = [
    # API urls
    path("api/", include("blog.api.urls")),
    # search results
    path("search", Search.as_view(), name="search"),
    # single post
    path("<slug:slug>", PostDetails.as_view(), name="post_details"),
    # all posts
    path("", Posts.as_view(), name="posts"),
]
