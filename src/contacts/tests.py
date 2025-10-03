from django.test import TestCase
from django.urls import reverse

from core.models import Reference

from .models import (
    Company, CompanyAddress,
    ContactType, CompanyContact,
    Contact
)

company_data = {
    Company.Field.short_name: "TestComp",
    Company.Field.full_name: "Full Company Name",
    Company.Field.registration: "RegNumber by RegDate",
    Company.Field.license: "LicenseNumber by LicenseDate",
}
company_address = {
    CompanyAddress.Field.country: "BY",
    CompanyAddress.Field.city: "Minsk",
    CompanyAddress.Field.zip_code: "220340",
    CompanyAddress.Field.street_address: "Novatorov street, 12, of.400"
}
company_contact_type = {
    Reference.Field.name: "e-mail",
    Reference.Field.description: "Preferred contact type"
}
company_contacts = [
    {
        CompanyContact.Field.contact_type: "e-mail",
        CompanyContact.Field.value: "test@email.com",
        CompanyContact.Field.description: "Primary contact"
    },
    {
        CompanyContact.Field.contact_type: "Telegram",
        CompanyContact.Field.value: "testogrammo",
        CompanyContact.Field.description: "Express contact"
    },
    {
        CompanyContact.Field.contact_type: "Phone",
        CompanyContact.Field.value: "+3752961121122",
        CompanyContact.Field.description: "Call center"
    }
]
user_messages = [
    {
        Contact.Field.contact_type: "e-mail",
        Contact.Field.author: "Peter Pan",
        Contact.Field.contact: "peter@neverhood.com",
        Contact.Field.text: "Please contact me ASAP"
    },
    {
        Contact.Field.contact_type: "Telegram",
        Contact.Field.author: "Incognito",
        Contact.Field.contact: "@Inco.gnito",
        Contact.Field.text: "I would like no stay unknown"
    },
    {
        Contact.Field.contact_type: "Phone",
        Contact.Field.author: "Zodiac",
        Contact.Field.contact: "+3280081275",
        Contact.Field.text: "Please contact me ASAP"
    }
]


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
        for company_contact in company_contacts:
            CompanyContact.objects.create(
                contact_type=ContactType.objects.create(
                    name=company_contact.get(
                        CompanyContact.Field.contact_type
                    )
                ),
                value=company_contact.get(
                    CompanyContact.Field.value
                ),
                company=company
            )

    def test_company_info(self) -> None:
        response = self.client.get(reverse("contacts:company_info"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contacts/contacts.html")

        for text in company_data.values():
            self.assertContains(response, text)

        for company_contact in company_contacts:
            self.assertContains(
                response,
                company_contact.get(
                    CompanyContact.Field.contact_type
                )
            )
            self.assertContains(
                response,
                company_contact.get(
                    CompanyContact.Field.value
                )
            )

        # Checking user contact form
        self.assertContains(response, "Your name:")
        self.assertContains(response, "Contact type:")
        self.assertContains(response, "Your contact:")
        self.assertContains(response, "Text:")
