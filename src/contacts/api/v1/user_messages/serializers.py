from rest_framework.serializers import (
    ModelSerializer, SerializerMethodField
)

from core.models import BaseModel

from ....models import Contact


class ContactSerializer(ModelSerializer):
    """
    Manages company contact object details serialization
    """

    class Meta:
        model = Contact
        fields = [
            Contact.Field.author,
            Contact.Field.contact_type,
            Contact.Field.contact,
            Contact.Field.text
            ]
        read_only_fields = [
            BaseModel.Field.id
        ]

        contact_type: SerializerMethodField = SerializerMethodField()

        def get_contact_type(self, instance):
            return instance.contact_type.id
