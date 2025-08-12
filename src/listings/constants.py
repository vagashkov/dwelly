from django.utils.translation import gettext_lazy as _

from core.models import BaseModel

LISTINGS_ORDERING = "{}".format(BaseModel.Field.created_at)

ERROR_KEY = "error"
ERROR_MSG_UNKNOWN_AMENITIES = _("Unknown amenities ids: {}")
ERROR_MSG_UNKNOWN_HOUSE_RULES = _("Unknown house rule ids: {}")
