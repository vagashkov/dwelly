from rest_framework.serializers import ModelSerializer

from core.models import Reference

from .....models import ContactType


class ContactTypeSerializer(ModelSerializer):
    """
    Manages company contact object details serialization
    """

    class Meta:
        model = ContactType
        fields = [
            Reference.Field.name,
            Reference.Field.description
            ]
