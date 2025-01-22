from django.contrib.auth.base_user import BaseUserManager


class AccountManager(BaseUserManager):
    """
    Custom user account manager where email is the unique identifier
    for authentication instead of username.
    """

    use_in_migrations: bool = True

    def create_user(self, email, password, **extra_fields):
        """
        Create and save account with the given email and password.
        """
        # Check if email is provided
        if not email:
            raise ValueError("User email cannot be empty")

        extra_fields.setdefault("is_active", True)
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_staff_user(self, email, password, **extra_fields):
        """
        Create and save staff account (moderator etc)
        with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)

        return self.create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
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
