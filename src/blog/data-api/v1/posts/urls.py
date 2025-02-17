from django.urls import path

from .views import Posts, PostDetails, PostCover

urlpatterns = [
    path(
        "<slug:slug>",
        PostDetails.as_view(),
        name="blog_api_post_details"
    ),
    path(
        "<slug:slug>/cover",
        PostCover.as_view(),
        name="blog_api_post_cover"
    ),
    path(
        "",
        Posts.as_view(),
        name="blog_api_posts"
    )
]
