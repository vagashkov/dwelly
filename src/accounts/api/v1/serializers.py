from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework.serializers import (
    Serializer, CharField, EmailField,
    ValidationError, as_serializer_error
)

from ...constants import (
    ERROR_MSG_DIFFERENT_PASSWORDS,
    ERROR_ALLAUTH_NOT_INSTALLED
)
from ...models import Account

try:
    from allauth.account.adapter import get_adapter
    from allauth.account.utils import setup_user_email
except ImportError:
    raise ImportError(ERROR_ALLAUTH_NOT_INSTALLED)


class PostSerializer(Serializer):
    """
    Manages account creation process
    """

    email: EmailField = EmailField(
        required=True,
        allow_blank=False,
        max_length=320
    )

    password1: CharField = CharField(
        required=True,
        allow_blank=False,
        write_only=True
    )

    password2: CharField = CharField(
        required=True,
        allow_blank=False,
        write_only=True
    )

    def validate(self, data):
        if data.get(
            "{}1".format(Account.Field.password)
            ) != data.get(
            "{}2".format(Account.Field.password)
        ):
            raise ValidationError(
                ERROR_MSG_DIFFERENT_PASSWORDS
            )

        return data

    def get_cleaned_data(self):
        # Needed for allauth adapter protocol compatibility
        return {
            Account.Field.email:
                self.validated_data.get(
                    Account.Field.email
                    ),
            "{}1".format(
                Account.Field.password
                ): self.validated_data.get(
                "{}1".format(
                    Account.Field.password
                    )
                )
            }

    def save(self, request):
        # Getting designated (almost always default) adapter
        adapter = get_adapter()

        # Create new CustomUser object
        user = adapter.new_user(request)

        # Prepare cleaned data
        self.cleaned_data = self.get_cleaned_data()

        # Update user base fields
        user = adapter.save_user(request, user, self, commit=False)

        # Set user password
        if "{}1".format(Account.Field.password) in self.cleaned_data:
            try:
                adapter.clean_password(
                    self.cleaned_data.get(
                        "{}1".format(
                            Account.Field.password
                        )
                    ),
                    user=user
                    )
            except DjangoValidationError as exc:
                raise ValidationError(
                    detail=as_serializer_error(exc)
                    )
        # And finally save new user to database
        user.save()

        # Perform other post-registration routines if necessary
        setup_user_email(request, user, [])

        # Finally return fresh made user object
        return user
