from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Comment, Postable


class CommentForm(ModelForm):
    """"
    Supports post commenting by registered users
    """

    class Meta:
        model = Comment
        fields = [
            Postable.Field.text
        ]
        labels = {
            Postable.Field.text: _("Comment:")
        }
