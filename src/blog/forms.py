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

    def __init__(self, *args: list, **kwargs: dict) -> None:
        super().__init__(*args, **kwargs)
        self.fields[
            Postable.Field.text
        ].widget.attrs.update(
            {
                "cols": "80",
                "rows": "4",
                "placeholder": _("Leave your comment here"),
                "class": "form-control"
            }
        )
