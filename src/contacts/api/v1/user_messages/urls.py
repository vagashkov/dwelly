from django.urls import path

from .views import ContactMessages, ContactMessageDetails

urlpatterns = [
    path(
        "<int:id>",
        ContactMessageDetails.as_view(),
        name="api_user_message_details"
    ),
    path(
        "",
        ContactMessages.as_view(),
        name="api_user_messages"
    )
]
