from django.urls import path, include

from .views import Posts, PostDetails


urlpatterns = [
    # API urls
    path("api/", include("blog.data-api.urls")),
    # single post
    path("<slug:slug>", PostDetails.as_view(), name="post_details"),
    # all posts
    path("", Posts.as_view(), name="blog_home"),
]
