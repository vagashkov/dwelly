from rest_framework.test import APITestCase

from users.models import User
from tests.test_data import good_user

email = good_user.get(User.Field.email)
password = good_user.get(User.Field.password)


class BaseAPITest(APITestCase):
    """
    Base class for amenities testing
    """

    def engage_user(self) -> None:
        # Create and login as standard user
        user = User.objects.create_user(
            email=email,
            password=password
        )

        # Login with standard account
        self.client.force_login(user)

    def engage_admin(self) -> None:
        # Create admin account
        admin = User.objects.create_superuser(
            email="admin-{}".format(email),
            password=password
        )

        # Login with admin account
        self.client.force_login(admin)
