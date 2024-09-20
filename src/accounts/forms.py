from django.contrib.auth.forms import BaseUserCreationForm
from django.forms import (
    EmailField
)

from .models import Account


class Signup(BaseUserCreationForm):
    """
    User registration form
    """

    class Meta:
        model = Account
        fields = (
            Account.Field.email,
        )

    email: EmailField = EmailField()
