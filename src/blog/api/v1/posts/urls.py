from django.urls import path

from .views import Posts, Search, PostDetails, PostCover
from .comments.views import Comments

urlpatterns = [
    path(
        "search",
        Search.as_view(),
        name="api_search"
    ),
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
