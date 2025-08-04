from django.urls import path

from .views import Posts, PostDetails, PostCover
from .comments.views import Comments

urlpatterns = [
    path(
        "<slug:slug>",
        PostDetails.as_view(),
        name="api_post_details"
    ),
    path(
        "<slug:slug>/cover",
        PostCover.as_view(),
        name="api_post_cover"
    ),
    path(
        "<slug:slug>/comments",
        Comments.as_view(),
        name="api_post_comments"
    ),
    path(
        "",
        Posts.as_view(),
        name="api_posts"
    )
]
