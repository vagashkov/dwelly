from django.contrib.auth import get_user_model

from rest_framework.serializers import (
    ModelSerializer, SerializerMethodField
)

from .....models import Postable, Comment

User = get_user_model()


class GetComments(ModelSerializer):
    """
    Manages existing comments serialization
    """

    class Meta:
        model = Comment
        fields = [
            Postable.Field.author,
            Postable.Field.text
            ]

    author = SerializerMethodField("get_author")

    def get_author(self, obj: User) -> str:
        return obj.author.email


class PostComment(ModelSerializer):
    """
    Manages new comment instance deserialization
    """

    class Meta:
        model = Comment
        fields = [
            Postable.Field.text
            ]
