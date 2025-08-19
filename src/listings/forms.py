from django.forms import ModelForm, DateInput
from django.utils.translation import gettext_lazy as _

from .models import Reservation


class DateOnlyInput(DateInput):
    input_type = "date"


class ReservationForm(ModelForm):
    """"
    Supports creating reservations by registered users
    """

    class Meta:
        model = Reservation
        fields = [
            Reservation.Field.check_in,
            Reservation.Field.check_out,
            Reservation.Field.comment
        ]
        labels = {
            Reservation.Field.check_in: _("Check-in date:"),
            Reservation.Field.check_out: _("Check-out date:"),
            Reservation.Field.comment: _("Comment:")
        }
        widgets = {
            Reservation.Field.check_in: DateOnlyInput(),
            Reservation.Field.check_out: DateOnlyInput(),
        }

    def __init__(self, *args: list, **kwargs: dict) -> None:
        super().__init__(*args, **kwargs)
        self.fields[
            Reservation.Field.comment
        ].widget.attrs.update(
            {
                "cols": "80",
                "rows": "4",
                "placeholder": _("Leave your comment here"),
                "class": "form-control"
            }
        )
        self.fields[
            Reservation.Field.check_in
        ].widget.attrs.update(
            {
                "class": "form-control",
                "width": 100
            }
        )
        self.fields[
            Reservation.Field.check_out
        ].widget.attrs.update(
            {
                "class": "form-control"
            }
        )
