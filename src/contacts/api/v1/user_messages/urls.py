from django.urls import path

from .views import UserMessages, UserMessageDetails

urlpatterns = [
    path(
        "<int:id>",
        UserMessageDetails.as_view(),
        name="api_user_message_details"
    ),
    path(
        "",
        UserMessages.as_view(),
        name="api_user_messages"
    )
]
