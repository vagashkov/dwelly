from django.urls import path

from .views import Posts, PostDetails


urlpatterns = [
    # all posts
    path("", Posts.as_view(), name="blog_home"),
    # single post
    path("<slug:slug>", PostDetails.as_view(), name="post_details"),
]
