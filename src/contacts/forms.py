from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Contact


class ContactForm(ModelForm):
    """"
    Supports post commenting by registered users
    """

    class Meta:
        model = Contact
        fields = [
            Contact.Field.author,
            Contact.Field.contact_type,
            Contact.Field.contact,
            Contact.Field.text
        ]
        labels = {
            Contact.Field.author: _("Your name:"),
            Contact.Field.contact_type: _("Contact type:"),
            Contact.Field.contact: _("Your contact:"),
            Contact.Field.text: _("Text:"),
        }

    def __init__(self, *args: list, **kwargs: dict) -> None:
        super().__init__(*args, **kwargs)
        self.fields[
            Contact.Field.text
        ].widget.attrs.update(
            {
                "cols": "80",
                "rows": "4",
                "placeholder": _("Leave your message here"),
                "class": "form-control"
            }
        )
