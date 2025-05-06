from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .models import User

from django.contrib.auth.base_user import BaseUserManager

from .constants import ERROR_MSG_NO_EMAIL


class UserManager(BaseUserManager):
    """
    Custom user manager where email is the unique identifier
    for authentication instead of username.
    """

    use_in_migrations: bool = True

    def create_user(
            self,
            email: str,
            password: str,
            **extra_fields: dict
    ) -> "User":
        """
        Create and save account with the given email and password.
        """
        # Check if email is provided
        if not email:
            raise ValueError(ERROR_MSG_NO_EMAIL)

        extra_fields.setdefault("is_active", True)
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_staff_user(
            self,
            email: str,
            password: str,
            **extra_fields: dict
    ) -> "User":
        """
        Create and save staff account (moderator etc)
        with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)

        return self.create_user(email, password, **extra_fields)

    def create_superuser(
            self,
            email: str,
            password: str,
            **extra_fields: dict
    ) -> "User":
        """
        Create and save a SuperUser (admin) with the given email and password.
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Admin must be staff member")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Admin must be superuser")

        return self.create_staff_user(email, password, **extra_fields)
