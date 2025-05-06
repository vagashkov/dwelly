from django.utils.translation import gettext_lazy as _

ERROR_KEY = "error"
ERROR_MSG_NO_EMAIL = _("User email is empty")
ERROR_MSG_DUPLICATE_MAIL = _("Email already exists")
ERROR_MSG_DIFFERENT_PASSWORDS = _("Password and it's confirmation don't match")
ERROR_ALLAUTH_NOT_INSTALLED = _("allauth needs to be added to INSTALLED_APPS.")
