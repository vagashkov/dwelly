from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework.serializers import (
    Serializer, ModelSerializer,
    CharField, EmailField,
    ValidationError, as_serializer_error
)

from ...constants import (
    ERROR_MSG_DUPLICATE_MAIL,
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

    def validate_email(self, email):
        try:
            Account.objects.get(
                email=email
            )
            raise ValidationError(
                ERROR_MSG_DUPLICATE_MAIL
            )
        except Account.DoesNotExist:
            return email

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

        # Create new Account object
        account = adapter.new_user(request)

        # Prepare cleaned data
        self.cleaned_data = self.get_cleaned_data()

        # Update user base fields
        account = adapter.save_user(
            request,
            account,
            self,
            commit=False
        )

        # Set account password
        if "password1" in self.cleaned_data:
            try:
                adapter.clean_password(
                    self.cleaned_data.get(
                        "password1"
                    ),
                    user=account
                    )
            except DjangoValidationError as exc:
                raise ValidationError(
                    detail=as_serializer_error(exc)
                    )
        # And finally save new account to database
        account.save()

        # Perform other post-registration routines if necessary
        setup_user_email(request, account, [])

        # Finally return fresh made account object
        return account


class ListSerializer(ModelSerializer):
    """
    Serializer for accounts list
    """

    class Meta:
        """
        """
        model = Account
        fields = [
            Account.Field.email,
            Account.Field.is_active,
            Account.Field.last_login
        ]


class DetailsSerializer(ModelSerializer):
    """
     Serializer for account details
    """

    class Meta:
        """
        """
        model = Account
        fields = [
            Account.Field.email,
            Account.Field.is_active,
            Account.Field.is_staff,
            Account.Field.is_superuser,
            Account.Field.date_joined,
            Account.Field.last_login
        ]
