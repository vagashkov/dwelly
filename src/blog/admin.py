from django.contrib.admin import (
    ModelAdmin, TabularInline, site
)
from django.forms import ModelForm

from tinymce.widgets import TinyMCE

from core.models import BaseModel
from .models import Tag, Status, Postable, Post, Comment


class CommentInline(TabularInline):
    model = Comment


class PostForm(ModelForm):
    """
    Manages new blog post creation
    """

    class Meta:
        model = Post
        fields = "__all__"
        widgets = {
            "text": TinyMCE(
                attrs={
                    "cols": 80,
                    "rows": 30
                }
            )
        }


class PostAdmin(ModelAdmin):
    list_display = (
        Post.Field.title,
        Postable.Field.author,
        BaseModel.Field.created_at
    )
    list_filter = (
        Post.Field.tags,
    )
    form = PostForm
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
