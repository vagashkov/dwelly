from django.contrib.admin import (
    ModelAdmin, TabularInline, site
)

from core.models import BaseModel
from .models import Tag, Status, Postable, Post, Comment


class CommentInline(TabularInline):
    model = Comment


class PostAdmin(ModelAdmin):
    list_display = (
        Post.Field.title,
        Postable.Field.author,
        BaseModel.Field.created_at
    )
    list_filter = (
        Post.Field.tags,
    )
    prepopulated_fields = {
        Post.Field.slug: (
            Post.Field.title,
        )
    }
    inlines = [
        CommentInline
    ]


class CommentAdmin(ModelAdmin):
    list_display = (
        Comment.Field.post,
        Postable.Field.author,
    )
    list_filter = (
        Comment.Field.post,
    )


site.register(Tag)
site.register(Status)
site.register(Post, PostAdmin)
site.register(Comment, CommentAdmin)
