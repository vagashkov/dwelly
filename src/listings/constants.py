from django.utils.translation import gettext_lazy as _

from core.models import BaseModel

LISTINGS_ORDERING = "{}".format(BaseModel.Field.created_at)

ERROR_KEY = "error"
ERROR_MSG_UNKNOWN_LISTING = _("Unknown listing slug: {}")
ERROR_MSG_UNKNOWN_AMENITIES = _("Unknown amenities ids: {}")
ERROR_MSG_UNKNOWN_HOUSE_RULES = _("Unknown house rule ids: {}")
ERROR_MSG_NEGATIVE_DAY_RATE = _("Rent price cannot be below zero: {}")
ERROR_MSG_OVERLAPPING_DATES = _("Some overlapping dates were found: {}")
ERROR_MSG_NO_FIXTURE = _("Source file {} doesn't exist")
ERROR_MSG_JSON_DECODING = _("JSON decode error: {}")

INFO_MSG_RESERVATION_STATUSES_LOADED = _(
    "Reservation statuses data loaded successfully"
)
