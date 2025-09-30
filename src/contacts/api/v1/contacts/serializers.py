from rest_framework.serializers import ModelSerializer

from ....models import CompanyContact


class ContactSerializer(ModelSerializer):
    """
    Manages company contact object details serialization
    """

    class Meta:
        model = CompanyContact
        fields = [
            CompanyContact.Field.contact_type,
            CompanyContact.Field.value,
            CompanyContact.Field.description
            ]
