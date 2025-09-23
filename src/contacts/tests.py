from django.test import TestCase
from django.urls import reverse

from .models import (
    Company, CompanyAddress,
    ContactType, CompanyContact
)

company_data = {
    "short_name": "TestComp",
    "full_name": "Full Company Name",
    "registration": "RegNumber by RegDate",
    "license": "LicenseNumber by LicenseDate",
}
company_address = {
    "country": "BY",
    "city": "Minsk",
    "zip_code": "220340",
    "street_address": "Novatorov street, 12, of.400"
}
company_contacts = {
        "e-mail": "test@email.com",
        "Telegram": "testogrammo",
        "Phone": "+3752961121122"
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

        company = Company.objects.create(
            **company_data
        )
        CompanyAddress.objects.create(
            **company_address,
            company=company
        )
        for contact_type, contact_value in company_contacts.items():
            CompanyContact.objects.create(
                contact_type=ContactType.objects.create(
                    name=contact_type
                ),
                value=contact_value,
                company=company
            )

    def test_posts_list(self) -> None:
        response = self.client.get(reverse("contacts:company_info"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contacts/contacts.html")

        for text in company_data.values():
            self.assertContains(response, text)

        for contact_type, contact_value in company_contacts.items():
            self.assertContains(response, contact_type)
            self.assertContains(response, contact_value)
