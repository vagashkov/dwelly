from django.urls import path, include

urlpatterns = [
    path(
        "v1/",
        include("blog.data-api.v1.urls")
    )
]
