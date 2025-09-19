from django.test import TestCase
from django.urls import reverse

from .models import Company

company_data = {
    "short_name": "TestComp",
    "full_name": "Full Company Name",
    "registration": "RegNumber by RegDate",
    "license": "LicenseNumber by LicenseDate"
}


class ContactsTest(TestCase):
    """
    Testing company info page
    """

    def setUp(self) -> None:
        """
        Prepare test data
        :return:
        """

        self.company = Company.objects.create(
            **company_data
        )

    def test_posts_list(self) -> None:
        response = self.client.get(reverse("contacts:company_info"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contacts/contacts.html")

        for text in company_data.values():
            self.assertContains(response, text)
