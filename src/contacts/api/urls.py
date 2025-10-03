from django.urls import path, include

urlpatterns = [
    path(
        "v1/",
        include("contacts.api.v1.urls")
    )
]
