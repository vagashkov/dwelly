from django.utils.translation import gettext_lazy as _

MSG_DB_AVAILABLE = _("Database connection established")
MSG_DB_NOT_AVAILABLE = _(
    "Database is still unavailable. Waiting for {} second(s)..."
)
MSG_INITIAL_STATUS_PREDECESSORS = _(
    "An initial status cannot have predecessors"
)
MSG_WRONG_MONTH_FORMAT = _(
    "<h2>Cannot interpret calendar month format (YYYYMM is needed)</h2>"
)
