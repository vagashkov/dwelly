from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework.request import Request
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

from ...models import User, Profile

try:
    from allauth.account.adapter import get_adapter
    from allauth.account.utils import setup_user_email
except ImportError:
    raise ImportError(ERROR_ALLAUTH_NOT_INSTALLED)


class UserPost(Serializer):
    """
    Manages user creation process
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

    def validate_email(self, email: str) -> str:
        try:
            User.objects.get(
                email=email
            )
            raise ValidationError(
                ERROR_MSG_DUPLICATE_MAIL
            )
        except User.DoesNotExist:
            return email

    def validate(self, data: dict) -> dict:
        if data.get(
            "{}1".format(User.Field.password)
            ) != data.get(
            "{}2".format(User.Field.password)
        ):
            raise ValidationError(
                ERROR_MSG_DIFFERENT_PASSWORDS
            )

        return data

    def get_cleaned_data(self) -> dict:
        # Needed for allauth adapter protocol compatibility
        return {
            User.Field.email:
                self.validated_data.get(
                    User.Field.email
                    ),
            "{}1".format(
                User.Field.password
                ): self.validated_data.get(
                "{}1".format(
                    User.Field.password
                    )
                )
            }

    def save(self, request: Request) -> User:
        # Getting designated (almost always default) adapter
        adapter = get_adapter()

        # Create new User object
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


class UserGet(ModelSerializer):
    """
    Serializer for getting single account details
    """

    class Meta:
        """
        """
        model = User
        fields = [
            User.Field.email,
            User.Field.is_active,
            User.Field.is_staff,
            User.Field.is_superuser,
            User.Field.date_joined,
            User.Field.last_login
        ]


class UsersList(ModelSerializer):
    """
    Serializer for accounts list
    """

    class Meta:
        """
        """
        model = User
        fields = [
            User.Field.email,
            User.Field.is_active,
            User.Field.last_login
        ]


class ProfilesList(ModelSerializer):
    """
    Serializer for profiles list
    """

    user = UsersList(required=True)

    class Meta:
        """
        """
        model = Profile
        fields = [
            Profile.Field.user,
            Profile.Field.full_name,
            Profile.Field.photo
        ]


class ProfileGet(ModelSerializer):
    """
    Serializer for getting single profile object details
    """

    user = UserGet(required=True)

    class Meta:
        """
        """
        model = Profile
        fields = [
            Profile.Field.user,
            Profile.Field.first_name,
            Profile.Field.last_name,
            Profile.Field.phone,
            Profile.Field.bio,
            Profile.Field.photo,
        ]


class ProfilePatch(ModelSerializer):
    """
    Serializer for single user data update
    """

    class Meta:
        """
        """
        model = Profile
        fields = [
            Profile.Field.first_name,
            Profile.Field.last_name,
            Profile.Field.phone,
            Profile.Field.bio,
            Profile.Field.photo,
        ]
