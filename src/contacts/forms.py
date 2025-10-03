from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import UserMessage


class ContactForm(ModelForm):
    """"
    Supports post commenting by registered users
    """

    class Meta:
        model = UserMessage
        fields = [
            UserMessage.Field.author,
            UserMessage.Field.contact_type,
            UserMessage.Field.contact,
            UserMessage.Field.text
        ]
        labels = {
            UserMessage.Field.author: _("Your name:"),
            UserMessage.Field.contact_type: _("Contact type:"),
            UserMessage.Field.contact: _("Your contact:"),
            UserMessage.Field.text: _("Text:"),
        }

    def __init__(self, *args: list, **kwargs: dict) -> None:
        super().__init__(*args, **kwargs)
        self.fields[
            UserMessage.Field.text
        ].widget.attrs.update(
            {
                "cols": "80",
                "rows": "4",
                "placeholder": _("Leave your message here"),
                "class": "form-control"
            }
        )
