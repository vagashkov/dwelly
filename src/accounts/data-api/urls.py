from django.urls import path, include

urlpatterns = [
    path(
        "v1/",
        include("accounts.data-api.v1.urls"),
    )
]
