from rest_framework.serializers import (
    ModelSerializer, SerializerMethodField
)

from ....models import Post, Postable


class GetRelatedFields(ModelSerializer):
    """
    Getting common related fields "humanized" values
    """

    author = SerializerMethodField("get_author")

    def get_author(self, obj: Post) -> str:
        return obj.author.email

    tags = SerializerMethodField("get_tags")

    def get_tags(self, obj: Post) -> list:
        return [
            tag.name for tag in obj.tags.all()
        ]


class GetListSerializer(GetRelatedFields):
    """
    Manages blog objects list serialization
    """

    class Meta:
        model = Post
        fields = [
            Post.Field.title,
            Postable.Field.author,
            Post.Field.excerpt,
            Post.Field.cover,
            Post.Field.tags,
            Post.Field.slug
            ]


class GetDetailsSerializer(GetRelatedFields):
    """
    Manages blog object details serialization
    """

    class Meta:
        model = Post
        fields = [
            Post.Field.title,
            Postable.Field.author,
            Post.Field.excerpt,
            Post.Field.cover,
            Post.Field.tags,
            Postable.Field.text
            ]


class PostSerializer(ModelSerializer):
    """
    Manages blog object creation
    """

    class Meta:
        model = Post
        fields = [
            Post.Field.title,
            Post.Field.excerpt,
            Post.Field.tags,
            Postable.Field.text
            ]
